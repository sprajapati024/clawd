# TOOLS.md - Day Trader Project Tools

## API Keys & Credentials

**Store in `~/.clawdbot/credentials/day-trader/` or environment variables**

### Required APIs
1. **Alpha Vantage** (free tier)
   - Key: `ALPHA_VANTAGE_API_KEY`
   - Rate limit: 5 calls/minute, 500 calls/day
   - Use for: Real-time quotes, technical indicators

2. **Yahoo Finance** (no key required)
   - Library: `yfinance` Python package
   - Use for: Historical data, fundamentals

3. **News API** (optional)
   - Provider: NewsAPI.org or RSS feeds
   - Use for: Market news, sentiment

### Telegram Integration
- Use main Clarke bot (same Telegram)
- Channel: `#day-trader-alerts` (optional separate chat)
- Format: Simple text + emoji alerts

## Python Environment

### Required Packages
```bash
pip install yfinance pandas numpy matplotlib requests
```

### Project Structure
```
day-trader/
├── data/                  # Market data storage
│   ├── historical/       # Daily price data
│   ├── portfolio/        # Portfolio snapshots
│   └── trades/          # Trade log
├── scripts/             # Automation scripts
│   ├── market_data.py   # Data collection
│   ├── portfolio.py     # Portfolio management
│   ├── alerts.py        # Alert generation
│   └── reporting.py     # Report generation
├── strategies/          # Trading strategies
│   ├── base.py         # Strategy base class
│   ├── swing_trade.py  # Swing trading logic
│   └── indicators.py   # Technical indicators
└── config/             # Configuration
    ├── symbols.json    # Watchlist
    └── settings.yaml   # Project settings
```

## Data Management

### File Formats
- **Portfolio:** CSV with columns: `symbol, shares, avg_price, current_price, pnl`
- **Trades:** CSV with columns: `date, symbol, action, shares, price, reason`
- **Performance:** JSON with daily snapshots

### Storage Locations
- Local: `/root/clawd/projects/day-trader/data/`
- Backup: Git commit daily
- Cloud: Optional S3/Backblaze backup

## Automation Scripts

### 1. Market Data Collector
```python
# scripts/market_data.py
# Runs at 4:05 PM EST daily
# Fetches: Daily prices, volume, indicators
# Stores: CSV files in data/historical/
```

### 2. Portfolio Updater
```python
# scripts/portfolio.py  
# Runs at 4:10 PM EST daily
# Updates: Current portfolio values
# Calculates: Daily P&L, performance metrics
```

### 3. Alert Generator
```python
# scripts/alerts.py
# Runs on demand or scheduled
# Checks: Stop losses, strategy signals
# Sends: Telegram alerts via Clawdbot
```

### 4. Report Generator
```python
# scripts/reporting.py
# Runs at 6:00 PM EST daily
# Generates: Daily performance report
# Creates: Simple charts/images
```

## Clawdbot Integration

### Skills to Build/Use
1. **Day Trader Monitor** - Portfolio check command
2. **Market Scanner** - Watchlist scanning
3. **Alert Manager** - Custom alert rules
4. **Report Sender** - Scheduled reports to Telegram

### Command Examples
```
/portfolio status      # Current portfolio snapshot
/market scan           # Scan watchlist for signals
/alert add TSLA <220   # Add price alert for TSLA under $220
/report daily          # Generate daily report
```

### Session Spawning
```bash
# Clarke spawns day-trader agent with project workspace
sessions_spawn \
  --task "Check portfolio performance" \
  --workspace /root/clawd/projects/day-trader
```

## Monitoring & Alerts

### Health Checks
- Daily data collection success/failure
- Portfolio calculation accuracy
- API rate limit monitoring
- Script execution logs

### Alert Channels
1. **Telegram** (primary) - Clarke bot
2. **Email** (optional) - Critical failures
3. **Log file** - `/var/log/day-trader/`

### Alert Examples
```
🟢 DAILY REPORT: Portfolio +2.3% ($230), TSLA +5%, AAPL -1%
🟡 ALERT: TSLA approaching stop loss at $210 (current $212)
🔴 STOP LOSS: AAPL hit stop at $175, selling 10 shares
```

## Development Notes

### Testing
- Use historical data for backtesting
- Paper trading before "live" simulation
- Validate all calculations manually first

### Safety
- No real money involved
- All trades simulated
- Maximum "loss" = learning opportunity
- Keep backups of all data

### Performance Tracking
- Benchmark vs S&P 500
- Track win/loss ratio
- Measure risk-adjusted returns
- Log all decisions for review

## Next Steps
1. Set up Python environment
2. Create basic data collection script
3. Build portfolio tracker
4. Integrate with Clarke for alerts
5. Add simple trading strategy
6. Create Telegram reporting