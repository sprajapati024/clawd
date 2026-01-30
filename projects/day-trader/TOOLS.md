# Day Trader Project - Tools & Scripts

## Overview
Autonomous trading bot system for algorithmic day trading with AI-powered decision making.

## Directory Structure
```
/root/clawd/projects/day-trader/
├── portfolio.py              # Portfolio management core
├── portfolio.csv            # Current holdings
├── trades.csv              # Trade history
├── cash.json               # Cash balance
├── scripts/
│   ├── trader.py           # Trading decision engine
│   ├── daily_routine.sh    # Daily automation script
│   └── portfolio_review.py # Portfolio review command
├── logs/                   # Daily logs and reports
├── backups/               # Data backups
└── TOOLS.md              # This file
```

## Core Components

### 1. Portfolio Management (`portfolio.py`)
**Purpose**: Manages holdings, cash, trades, and performance tracking.

**Key Functions**:
- `buy(symbol, shares, price, reasoning)`: Buy shares with risk checks
- `sell(symbol, shares, price, reasoning)`: Sell shares with risk checks
- `get_portfolio()`: Get current holdings
- `get_performance()`: Get performance metrics
- `update_prices(price_updates)`: Update current prices

**Risk Management**:
- Max position size: 10% of portfolio
- Stop loss: 5% (configurable)
- Take profit: 10% (configurable)

### 2. Trading Decision Engine (`scripts/trader.py`)
**Purpose**: AI-powered trading decisions using DeepSeek API.

**Features**:
- Technical + fundamental analysis
- Risk-managed trade recommendations
- Real-time market analysis
- Trade execution with risk checks

**Configuration**:
- API: DeepSeek via OpenRouter
- Model: `deepseek/deepseek-chat`
- Temperature: 0.3 (conservative)

### 3. Daily Routine (`scripts/daily_routine.sh`)
**Purpose**: Automated daily trading workflow.

**Schedule**: Runs at 4:30 PM EST (after market close)

**Steps**:
1. Check market status
2. Fetch latest prices
3. Update portfolio prices
4. Run trading analysis
5. Execute trades
6. Generate daily report
7. Backup data
8. Send notifications (optional)

**Logging**: Daily logs in `logs/daily_YYYYMMDD.log`

### 4. Portfolio Review (`scripts/portfolio_review.py`)
**Purpose**: Generate Telegram-friendly portfolio summaries.

**Usage**:
```bash
# Basic summary
python3 scripts/portfolio_review.py

# With S&P 500 comparison
python3 scripts/portfolio_review.py --benchmark

# Simple output (no emojis)
python3 scripts/portfolio_review.py --simple
```

**Output Format**:
- Clean text (no tables)
- Emoji-enhanced for readability
- Performance metrics
- Current holdings
- Recent trades
- Risk metrics

## API Keys Required

### Essential:
1. **DeepSeek API Key** (OpenRouter)
   - For trading decisions
   - Get from: https://openrouter.ai/keys

### Optional:
2. **Telegram Bot Token**
   - For notifications
   - Create via @BotFather

3. **Financial Data APIs** (for future enhancement)
   - Alpha Vantage, Polygon, etc.

## Setup Instructions

### 1. Initial Setup:
```bash
cd /root/clawd/projects/day-trader

# Make scripts executable
chmod +x scripts/*.py scripts/*.sh

# Test portfolio system
python3 portfolio.py
```

### 2. Configure API Keys:
Edit `/root/clawd-workspace/dexter/.env`:
```bash
DEEPSEEK_API_KEY=your_openrouter_api_key_here
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 3. Test Trading Engine:
```bash
cd /root/clawd/projects/day-trader
python3 scripts/trader.py
```

### 4. Test Daily Routine:
```bash
cd /root/clawd/projects/day-trader
bash scripts/daily_routine.sh
```

### 5. Test Portfolio Review:
```bash
cd /root/clawd/projects/day-trader
python3 scripts/portfolio_review.py
```

## Automation Setup

### Option A: Cron Job (Recommended)
```bash
# Edit crontab
crontab -e

# Add this line (runs at 4:30 PM EST daily)
30 16 * * 1-5 cd /root/clawd/projects/day-trader && bash scripts/daily_routine.sh >> /root/clawd/projects/day-trader/logs/cron.log 2>&1
```

### Option B: Heartbeat Integration
Add to `HEARTBEAT.md`:
```markdown
## Daily Trading Check
- [ ] Run daily trading routine at 4:30 PM EST
- [ ] Check portfolio performance
- [ ] Review recent trades
```

## Clawdbot Integration

### Portfolio Command Wrapper
Create a Clawdbot skill for `/portfolio` command:

```python
# Example skill structure
# /root/clawd/skills/portfolio/skill.py

from scripts.portfolio_review import PortfolioReview

def portfolio_command():
    review = PortfolioReview()
    return review.generate_summary()
```

### Telegram Integration
The daily routine can send Telegram notifications when configured:
- Daily completion status
- Portfolio performance
- Trade executions
- Error alerts

## Data Files

### `portfolio.csv`
```csv
symbol,shares,avg_price,current_price,market_value,pnl
AAPL,10,150.00,155.00,1550.00,50.00
```

### `trades.csv`
```csv
timestamp,symbol,action,shares,price,reasoning
2024-01-30T16:30:00,AAPL,BUY,10,150.00,Technical breakout
```

### `cash.json`
```json
{
  "cash": 8500.00,
  "last_updated": "2024-01-30T16:30:00"
}
```

## Monitoring & Maintenance

### Log Files:
- `logs/daily_YYYYMMDD.log`: Daily execution logs
- `logs/report_YYYYMMDD.txt`: Daily performance reports
- `logs/cron.log`: Cron job output

### Backups:
- Automatic daily backups in `backups/`
- Kept for 30 days
- Manual restore: `tar -xzf backup_YYYYMMDD_HHMMSS.tar.gz`

### Health Checks:
1. Check log files for errors
2. Verify API key validity
3. Monitor disk space for backups
4. Review trade execution success rate

## Troubleshooting

### Common Issues:

1. **API Key Errors**:
   - Verify `.env` file permissions
   - Check API key validity
   - Test with curl: `curl -H "Authorization: Bearer $KEY" https://openrouter.ai/api/v1/models`

2. **Permission Errors**:
   ```bash
   chmod +x scripts/*.py scripts/*.sh
   chmod 644 portfolio.csv trades.csv cash.json
   ```

3. **Cron Job Not Running**:
   - Check system timezone: `timedatectl`
   - Verify cron service: `systemctl status cron`
   - Check cron logs: `grep CRON /var/log/syslog`

4. **Data Corruption**:
   - Restore from latest backup
   - Check file permissions
   - Validate CSV/JSON format

## Future Enhancements

### Phase 2:
1. Real market data integration
2. Advanced technical indicators
3. Multi-timeframe analysis
4. Portfolio optimization

### Phase 3:
1. Machine learning models
2. Sentiment analysis
3. Options trading
4. Risk parity strategies

## Support
- Check logs first: `tail -f logs/daily_$(date +%Y%m%d).log`
- Review recent trades: `tail -20 trades.csv`
- Test components individually
- Backup before major changes