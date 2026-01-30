---
name: day-trader
description: Autonomous trading bot portfolio review and management
metadata: {"clawdbot":{"emoji":"📊","os":["linux"]}}
---

# Day Trader Skill

Autonomous trading bot that makes simulated trades Mon-Fri and provides portfolio reviews.

## Commands

### Portfolio Review
```bash
cd /root/clawd/projects/day-trader && python3 scripts/portfolio_review.py
```

Shows:
- Current holdings and values
- Profit/loss ($ and %)
- Recent trades with reasoning
- Risk metrics
- Closing balance

### Manual Trade Execution
```bash
cd /root/clawd/projects/day-trader && python3 -c "
from portfolio import buy, sell
buy('SYMBOL', SHARES, PRICE, 'reasoning')
sell('SYMBOL', SHARES, PRICE, 'reasoning')
"
```

### Daily Routine (Manual Trigger)
```bash
cd /root/clawd/projects/day-trader && bash scripts/daily_routine.sh
```

## Automation

Runs automatically Mon-Fri at 4:30 PM EST via cron:
- Fetches latest prices
- Analyzes market data
- Makes autonomous trade decisions
- Generates daily report
- Sends Telegram notification

## Files

- `portfolio.csv` - Current holdings
- `trades.csv` - Trade history
- `cash.json` - Cash balance
- `logs/report_YYYYMMDD.txt` - Daily reports
- `logs/daily_YYYYMMDD.log` - Execution logs

## API Keys Required

Add to `/root/clawd-workspace/dexter/.env`:
- `DEEPSEEK_API_KEY` - For trading decisions (OpenRouter)
- `FINANCIAL_DATASETS_API_KEY` - For real market data (optional)
- `TAVILY_API_KEY` - For news/research (optional)

## Starting Capital

$10,000 CAD (simulation only)
