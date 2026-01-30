# Autonomous Trading Bot - Installation Guide

## Quick Start

### 1. Clone/Setup Project
```bash
# Project is already at /root/clawd/projects/day-trader/
cd /root/clawd/projects/day-trader

# Make scripts executable
chmod +x scripts/*.py scripts/*.sh
```

### 2. Test Basic Functionality
```bash
# Test portfolio system
python3 portfolio.py

# Test portfolio review
python3 scripts/portfolio_review.py

# Run system test
python3 test_system.py
```

### 3. Configure API Keys
Edit `/root/clawd-workspace/dexter/.env`:
```bash
# Essential for AI trading decisions
DEEPSEEK_API_KEY=your_openrouter_api_key_here

# Optional for notifications
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 4. Set Up Automation
```bash
# Add to crontab (runs at 4:30 PM EST Mon-Fri)
crontab -e

# Add this line:
30 16 * * 1-5 cd /root/clawd/projects/day-trader && bash scripts/daily_routine.sh >> /root/clawd/projects/day-trader/logs/cron.log 2>&1
```

## Detailed Setup

### Prerequisites
- Python 3.8+
- Bash shell
- Cron service (for automation)

### File Structure
```
/root/clawd/projects/day-trader/
├── portfolio.py              # Core portfolio management
├── scripts/
│   ├── trader.py            # AI trading engine
│   ├── daily_routine.sh     # Daily automation
│   └── portfolio_review.py  # Portfolio summaries
├── logs/                    # Logs and reports
├── backups/                 # Data backups
└── TOOLS.md                # Complete documentation
```

### API Key Configuration

#### 1. DeepSeek API (Required)
1. Sign up at [OpenRouter.ai](https://openrouter.ai/)
2. Get your API key from [Keys page](https://openrouter.ai/keys)
3. Add to `.env`:
   ```
   DEEPSEEK_API_KEY=sk-or-v1-...
   ```

#### 2. Telegram Bot (Optional)
1. Create bot via [@BotFather](https://t.me/botfather)
2. Get your `TELEGRAM_BOT_TOKEN`
3. Get your `TELEGRAM_CHAT_ID` (send message to @userinfobot)
4. Add to `.env`:
   ```
   TELEGRAM_BOT_TOKEN=1234567890:ABCdef...
   TELEGRAM_CHAT_ID=987654321
   ```

### Testing

#### Basic Tests
```bash
# Test portfolio management
cd /root/clawd/projects/day-trader
python3 -c "from portfolio import buy, sell, get_performance; print('Portfolio system ready')"

# Test trading engine (without API key)
python3 scripts/trader.py

# Test daily routine (dry run)
bash scripts/daily_routine.sh
```

#### Integration Test
```bash
# Full system test
python3 test_system.py
```

### Automation Setup

#### Option A: Cron Job (Recommended)
```bash
# Edit crontab
crontab -e

# Add for 4:30 PM EST (16:30 UTC-5) Monday-Friday
30 16 * * 1-5 cd /root/clawd/projects/day-trader && bash scripts/daily_routine.sh >> /root/clawd/projects/day-trader/logs/cron.log 2>&1

# Verify cron job
crontab -l
```

#### Option B: Manual Execution
```bash
# Run daily routine manually
cd /root/clawd/projects/day-trader
bash scripts/daily_routine.sh
```

### Clawdbot Integration

#### Portfolio Command
The system includes a Clawdbot skill wrapper at `portfolio_skill.py`.

To integrate with Clawdbot:
1. Copy `portfolio_skill.py` to your Clawdbot skills directory
2. Register the command in your Clawdbot configuration
3. Use `/portfolio` command in Telegram

#### Manual Portfolio Review
```bash
# Basic summary
python3 scripts/portfolio_review.py

# With S&P 500 comparison
python3 scripts/portfolio_review.py --benchmark

# Simple text output
python3 scripts/portfolio_review.py --simple
```

## Monitoring & Maintenance

### Log Files
- Check daily logs: `tail -f logs/daily_$(date +%Y%m%d).log`
- View cron output: `tail -f logs/cron.log`
- See reports: `cat logs/report_$(date +%Y%m%d).txt`

### Data Files
- Portfolio: `portfolio.csv`
- Trade history: `trades.csv`
- Cash balance: `cash.json`

### Backups
- Automatic daily backups in `backups/`
- Manual backup: `tar -czf backup_$(date +%Y%m%d).tar.gz portfolio.csv trades.csv cash.json`
- Restore: `tar -xzf backup_YYYYMMDD.tar.gz`

## Troubleshooting

### Common Issues

#### 1. Permission Errors
```bash
chmod +x scripts/*.py scripts/*.sh
chmod 644 portfolio.csv trades.csv cash.json
```

#### 2. API Key Issues
- Verify `.env` file exists and has correct permissions
- Test API key: `curl -H "Authorization: Bearer $DEEPSEEK_API_KEY" https://openrouter.ai/api/v1/models`
- Check for typos in API key

#### 3. Cron Job Not Running
```bash
# Check cron service
systemctl status cron

# Check cron logs
grep CRON /var/log/syslog

# Verify timezone
timedatectl
```

#### 4. Script Errors
```bash
# Check Python version
python3 --version

# Test individual components
python3 -c "import csv; import json; print('Modules available')"

# Run with debug
bash -x scripts/daily_routine.sh
```

## Next Steps

### Phase 1: Basic Setup ✓
- [x] Portfolio management system
- [x] AI trading engine
- [x] Daily automation script
- [x] Portfolio review command
- [x] Documentation

### Phase 2: Enhancements
1. **Real Market Data**
   - Integrate Alpha Vantage/Polygon API
   - Real-time price updates
   - Historical data analysis

2. **Advanced Features**
   - Technical indicators (RSI, MACD, etc.)
   - Multi-timeframe analysis
   - Portfolio optimization

3. **Risk Management**
   - Dynamic position sizing
   - Correlation analysis
   - Drawdown protection

### Phase 3: Production Ready
1. **Monitoring**
   - Health checks
   - Performance metrics
   - Alert system

2. **Backtesting**
   - Historical simulation
   - Strategy validation
   - Parameter optimization

3. **Deployment**
   - Docker container
   - CI/CD pipeline
   - Multi-environment support

## Support

### Quick Reference
- System test: `python3 test_system.py`
- Portfolio review: `python3 scripts/portfolio_review.py`
- Daily routine: `bash scripts/daily_routine.sh`
- Logs: `logs/daily_$(date +%Y%m%d).log`

### Documentation
- Complete guide: `TOOLS.md`
- Installation: `INSTALL.md` (this file)
- Code documentation in each script

### Getting Help
1. Check logs first
2. Run system test
3. Review configuration
4. Consult documentation