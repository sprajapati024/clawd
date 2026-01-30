#!/bin/bash
#
# Daily Trading Routine
# Runs at 4:30 PM EST (after market close)
#

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/daily_$(date +%Y%m%d).log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create log directory
mkdir -p "$LOG_DIR"

# Log function
log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case $level in
        INFO) color=$GREEN ;;
        WARN) color=$YELLOW ;;
        ERROR) color=$RED ;;
        *) color=$NC ;;
    esac
    
    echo -e "${color}[$timestamp] [$level] $message${NC}" | tee -a "$LOG_FILE"
}

# Error handling
trap 'log ERROR "Script failed at line $LINENO"; exit 1' ERR

log INFO "=========================================="
log INFO "DAILY TRADING ROUTINE STARTED"
log INFO "Date: $(date)"
log INFO "=========================================="

# Check if it's a weekday (Mon-Fri)
DAY_OF_WEEK=$(date +%u)  # 1=Monday, 7=Sunday
if [ "$DAY_OF_WEEK" -gt 5 ]; then
    log INFO "Weekend detected (day $DAY_OF_WEEK). Markets closed. Exiting."
    exit 0
fi

# Step 1: Check market status
log INFO "Step 1: Checking market status..."
MARKET_STATUS="closed"  # Assuming 4:30 PM EST = market closed
log INFO "Market status: $MARKET_STATUS"

# Step 2: Fetch latest prices (mock for now)
log INFO "Step 2: Fetching latest prices..."
# In production, this would use a real API
# For now, we'll generate mock prices
python3 -c "
import random
from datetime import datetime

symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'BRK.B', 'JPM', 'V']
prices = {}

for symbol in symbols:
    # Generate realistic-ish mock prices
    if symbol == 'AAPL':
        base = 150 + random.uniform(-5, 5)
    elif symbol == 'MSFT':
        base = 300 + random.uniform(-10, 10)
    elif symbol == 'GOOGL':
        base = 140 + random.uniform(-5, 5)
    elif symbol == 'AMZN':
        base = 170 + random.uniform(-5, 5)
    elif symbol == 'TSLA':
        base = 180 + random.uniform(-10, 10)
    elif symbol == 'NVDA':
        base = 120 + random.uniform(-20, 20)
    else:
        base = 100 + random.uniform(-20, 20)
    
    prices[symbol] = round(base, 2)

print('Mock prices generated for:', ', '.join(symbols))
for symbol, price in prices.items():
    print(f'{symbol}: \${price:.2f}')

# Save to file for portfolio update
import json
with open('/tmp/latest_prices.json', 'w') as f:
    json.dump({'timestamp': datetime.now().isoformat(), 'prices': prices}, f)
"

if [ -f "/tmp/latest_prices.json" ]; then
    log INFO "Prices saved to /tmp/latest_prices.json"
else
    log WARN "Price generation may have failed"
fi

# Step 3: Update portfolio with latest prices
log INFO "Step 3: Updating portfolio prices..."
if [ -f "/tmp/latest_prices.json" ]; then
    python3 -c "
import json
from portfolio import update_prices

with open('/tmp/latest_prices.json', 'r') as f:
    data = json.load(f)

update_prices(data['prices'])
print(f\"Updated prices for {len(data['prices'])} symbols\")
"
    log INFO "Portfolio prices updated"
else
    log WARN "Skipping price update - no price file"
fi

# Step 4: Run trading analysis
log INFO "Step 4: Running trading analysis..."
ANALYSIS_OUTPUT=$(python3 "$SCRIPT_DIR/trader.py" 2>&1)
ANALYSIS_EXIT=$?

if [ $ANALYSIS_EXIT -eq 0 ]; then
    log INFO "Trading analysis completed successfully"
    echo "$ANALYSIS_OUTPUT" >> "$LOG_FILE"
    
    # Check if trades were executed
    if echo "$ANALYSIS_OUTPUT" | grep -q "Executed.*trades"; then
        TRADES_COUNT=$(echo "$ANALYSIS_OUTPUT" | grep -o "Executed [0-9]* trades" | grep -o "[0-9]*")
        log INFO "Trades executed: $TRADES_COUNT"
    else
        log INFO "No trades executed"
    fi
else
    log ERROR "Trading analysis failed with exit code $ANALYSIS_EXIT"
    echo "$ANALYSIS_OUTPUT" >> "$LOG_FILE"
fi

# Step 5: Generate daily report
log INFO "Step 5: Generating daily report..."
REPORT_FILE="$LOG_DIR/report_$(date +%Y%m%d).txt"
python3 -c "
import sys
from portfolio import get_performance, get_recent_trades
from datetime import datetime

perf = get_performance()
trades = get_recent_trades(5)
report_file = '$REPORT_FILE'

with open(report_file, 'w') as f:
    f.write('DAILY TRADING REPORT\\n')
    f.write('=' * 50 + '\\n')
    f.write(f'Date: {datetime.now().strftime(\"%Y-%m-%d %H:%M:%S EST\")}\\n\\n')
    
    f.write('PORTFOLIO SUMMARY\\n')
    f.write('-' * 30 + '\\n')
    f.write(f'Cash: \${perf[\"cash\"]:.2f}\\n')
    f.write(f'Invested: \${perf[\"invested\"]:.2f}\\n')
    f.write(f'Market Value: \${perf[\"market_value\"]:.2f}\\n')
    f.write(f'Total Value: \${perf[\"total_value\"]:.2f}\\n')
    f.write(f'Total P&L: \${perf[\"total_pnl\"]:.2f}\\n')
    f.write(f'Total Return: \${perf[\"total_return\"]:.2f} ({perf[\"total_return_pct\"]:.2f}%)\\n\\n')
    
    f.write('RECENT TRADES (Last 5)\\n')
    f.write('-' * 30 + '\\n')
    if trades:
        for trade in trades:
            f.write(f'{trade[\"timestamp\"]}: {trade[\"action\"]} {trade[\"shares\"]} {trade[\"symbol\"]} @ \${trade[\"price\"]:.2f}\\n')
            if trade[\"reasoning\"]:
                f.write(f'  Reason: {trade[\"reasoning\"]}\\n')
    else:
        f.write('No recent trades\\n')

print(f'Report saved to {report_file}')
"

if [ -f "$REPORT_FILE" ]; then
    log INFO "Daily report generated: $REPORT_FILE"
    # Show summary
    echo ""
    tail -20 "$REPORT_FILE"
else
    log ERROR "Failed to generate daily report"
fi

# Step 6: Backup data
log INFO "Step 6: Backing up data..."
BACKUP_DIR="$PROJECT_DIR/backups"
mkdir -p "$BACKUP_DIR"
BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).tar.gz"

tar -czf "$BACKUP_FILE" \
    "$PROJECT_DIR/portfolio.csv" \
    "$PROJECT_DIR/trades.csv" \
    "$PROJECT_DIR/cash.json" \
    "$LOG_DIR" 2>/dev/null || true

if [ -f "$BACKUP_FILE" ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    log INFO "Backup created: $BACKUP_FILE ($BACKUP_SIZE)"
else
    log WARN "Backup creation may have failed"
fi

# Step 7: Cleanup old logs (keep 7 days)
log INFO "Step 7: Cleaning up old logs..."
find "$LOG_DIR" -name "daily_*.log" -mtime +7 -delete 2>/dev/null || true
find "$LOG_DIR" -name "report_*.txt" -mtime +7 -delete 2>/dev/null || true
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +30 -delete 2>/dev/null || true

log INFO "=========================================="
log INFO "DAILY ROUTINE COMPLETED SUCCESSFULLY"
log INFO "=========================================="

# Send Telegram notification using TelegramReporter (if configured)
if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
    log INFO "Sending Telegram notification via TelegramReporter..."
    
    # Use Python to generate proper Telegram report
    python3 -c "
import sys
sys.path.insert(0, '$PROJECT_DIR')
from telegram_reporter import TelegramReporter
from portfolio import get_performance
import json

# Initialize reporter
reporter = TelegramReporter(bot_token='$TELEGRAM_BOT_TOKEN', chat_id='$TELEGRAM_CHAT_ID')

# Get portfolio data
portfolio_data = get_performance()

# Read trade results from analysis file
trade_data = {'executed_trades': [], 'skipped_trades': [], 'errors': [], 'summary': {'total_recommendations': 0, 'executed': 0, 'skipped': 0, 'failed': 0}}
analysis_data = {'market_condition': 'unknown', 'market_summary': 'Analysis completed', 'trade_recommendations': [], 'analysis_source': 'daily_routine'}

try:
    # Try to read analysis results
    with open('$PROJECT_DIR/logs/analysis_results.json', 'r') as f:
        analysis_results = json.load(f)
        trade_data = analysis_results.get('trade_results', trade_data)
        analysis_data.update(analysis_results.get('market_analysis', {}))
except:
    pass

# Generate and send daily summary
summary = reporter.format_daily_summary(portfolio_data, trade_data, analysis_data)
success = reporter.send_message(summary)

if success:
    print('✅ Telegram notification sent successfully')
else:
    print('⚠️ Failed to send Telegram notification')
" || log WARN "Failed to send Telegram notification via TelegramReporter"
fi

exit 0