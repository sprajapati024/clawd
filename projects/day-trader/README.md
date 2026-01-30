# Autonomous Trading Bot System

## 🚀 Overview
A fully automated day trading bot system with AI-powered decision making, portfolio management, and risk controls.

## ✨ Features

### Core Components
- **Portfolio Management**: Track holdings, cash, trades, and performance
- **AI Trading Engine**: DeepSeek-powered market analysis and trade decisions
- **Daily Automation**: Scheduled trading routine (4:30 PM EST)
- **Risk Management**: Position limits, stop losses, take profits
- **Telegram Integration**: Portfolio reviews and notifications

### Key Benefits
- 🤖 **Fully Autonomous**: Runs daily without manual intervention
- 🧠 **AI-Powered**: Uses DeepSeek for intelligent trading decisions
- 📊 **Risk Managed**: Strict position limits and risk controls
- 📱 **Telegram Ready**: Clean portfolio summaries and notifications
- 🔄 **Automated Backups**: Daily data backup and log rotation

## 📁 Project Structure
```
/root/clawd/projects/day-trader/
├── portfolio.py              # Portfolio management core
├── scripts/
│   ├── trader.py            # AI trading decision engine
│   ├── daily_routine.sh     # Daily automation script
│   └── portfolio_review.py  # Portfolio review command
├── logs/                    # Execution logs and reports
├── backups/                 # Data backups
├── TOOLS.md                # Complete documentation
├── INSTALL.md              # Installation guide
└── test_system.py          # System test
```

## 🚦 Quick Start

### 1. Test the System
```bash
cd /root/clawd/projects/day-trader
python3 test_system.py
```

### 2. Configure API Keys
Edit `/root/clawd-workspace/dexter/.env`:
```bash
DEEPSEEK_API_KEY=your_openrouter_api_key_here
```

### 3. Set Up Automation
```bash
# Add to crontab (runs at 4:30 PM EST Mon-Fri)
crontab -e
# Add: 30 16 * * 1-5 cd /root/clawd/projects/day-trader && bash scripts/daily_routine.sh >> logs/cron.log 2>&1
```

## 📊 Portfolio Review
```bash
# Basic summary
python3 scripts/portfolio_review.py

# With S&P 500 comparison
python3 scripts/portfolio_review.py --benchmark

# Simple text output
python3 scripts/portfolio_review.py --simple
```

## ⚙️ Configuration

### Risk Parameters
- **Max Position Size**: 10% of portfolio
- **Stop Loss**: 5% per position
- **Take Profit**: 10% per position
- **Initial Capital**: $10,000 CAD

### Trading Schedule
- **Analysis Time**: 4:30 PM EST (after market close)
- **Trading Days**: Monday-Friday
- **Data Backup**: Daily automatic backups

## 🔧 Integration

### Clawdbot Skill
Use `/portfolio` command in Telegram:
- `/portfolio` - Basic portfolio summary
- `/portfolio benchmark` - Include S&P 500 comparison
- `/portfolio simple` - Simple text (no emojis)

### Telegram Notifications
Optional Telegram notifications for:
- Daily routine completion
- Trade executions
- Portfolio performance
- Error alerts

## 📈 Performance Tracking

### Metrics Tracked
- Cash balance and allocation
- Portfolio value and P&L
- Total return vs initial capital
- Position-level performance
- Trade history and reasoning

### Reports Generated
- Daily execution logs
- Portfolio performance reports
- Trade execution summaries
- Risk metrics analysis

## 🛡️ Risk Management

### Position Limits
- No single position > 10% of portfolio
- Cash reserve maintained
- Diversification encouraged

### Trade Validation
- Sufficient cash check
- Position size validation
- Price validation
- Reason logging

### Data Protection
- Daily automatic backups
- Log rotation (7 days)
- Backup retention (30 days)
- Error recovery mechanisms

## 🔍 Monitoring

### Log Files
- `logs/daily_YYYYMMDD.log` - Daily execution logs
- `logs/report_YYYYMMDD.txt` - Daily performance reports
- `logs/cron.log` - Cron job output

### Health Checks
- API connectivity
- File permissions
- Disk space
- Backup integrity

## 🚨 Troubleshooting

### Common Issues
1. **API Key Errors**: Verify `.env` file and key validity
2. **Permission Errors**: Run `chmod +x scripts/*.py scripts/*.sh`
3. **Cron Issues**: Check `systemctl status cron` and timezone
4. **Data Issues**: Restore from `backups/` directory

### Debug Commands
```bash
# Test portfolio system
python3 portfolio.py

# Test trading engine
python3 scripts/trader.py

# Test daily routine
bash scripts/daily_routine.sh

# Check logs
tail -f logs/daily_$(date +%Y%m%d).log
```

## 📚 Documentation

### Complete Guides
- **TOOLS.md**: Detailed system documentation
- **INSTALL.md**: Step-by-step installation guide
- **Code Comments**: Inline documentation in all scripts

### API Reference
- Portfolio functions: `buy()`, `sell()`, `get_performance()`, etc.
- Trading engine: `analyze_market()`, `execute_trades()`
- Review command: `generate_summary()`, `compare_to_sp500()`

## 🎯 Roadmap

### Phase 1: Core System ✓
- [x] Portfolio management
- [x] AI trading engine
- [x] Daily automation
- [x] Basic risk management

### Phase 2: Enhanced Features
- [ ] Real market data integration
- [ ] Technical indicators
- [ ] Advanced risk analytics
- [ ] Multi-account support

### Phase 3: Production Ready
- [ ] Docker deployment
- [ ] Web dashboard
- [ ] Advanced backtesting
- [ ] Multi-strategy support

## 🤝 Support

### Getting Help
1. Check `logs/` directory for error details
2. Run `python3 test_system.py` for system validation
3. Review `TOOLS.md` for complete documentation
4. Check cron logs: `grep CRON /var/log/syslog`

### Contributing
This is a production system for automated trading. For enhancements:
1. Test changes with `test_system.py`
2. Backup data before modifications
3. Update documentation in `TOOLS.md`
4. Validate risk parameters remain conservative

## 📄 License
Proprietary trading system - For authorized use only.

---
**Status**: ✅ Production Ready  
**Last Tested**: System test passed  
**Next Analysis**: 4:30 PM EST daily  
**Support**: Check logs and documentation first