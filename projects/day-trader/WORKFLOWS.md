# WORKFLOWS.md - Day Trader Automation

## Daily Routine (Automated)

### 6:00 AM EST - Pre-market scan
- Check overnight news (RSS feeds)
- Scan watchlist for gap ups/downs
- Update economic calendar events

### 9:30 AM EST - Market open
- Monitor opening volatility
- Check for unusual volume
- Execute any pending orders

### 12:00 PM EST - Midday check
- Portfolio performance snapshot
- Strategy performance review
- Adjust stop losses if needed

### 4:00 PM EST - Market close
- Daily performance report
- Update portfolio values
- Log trades/decisions
- Prepare next day watchlist

## Weekly Routines

### Sunday 8:00 PM EST - Weekly planning
- Review past week performance
- Adjust strategies based on results
- Set weekly goals/targets
- Update watchlist

### Friday 4:30 PM EST - Weekly review
- Portfolio performance vs benchmarks
- Strategy effectiveness analysis
- Risk assessment
- Lessons learned

## Trading Workflows

### 1. New Position Entry
```
Trigger: Strategy signal + risk check
Steps:
1. Check available capital
2. Calculate position size (risk management)
3. Set entry price/limit
4. Place "order" (simulated)
5. Set stop loss/take profit
6. Log trade in portfolio
```

### 2. Position Management
```
Daily:
- Check stop losses
- Monitor news for holdings
- Adjust trailing stops if active

Exit triggers:
- Take profit hit
- Stop loss triggered
- Strategy exit signal
- Time-based exit (swing trade)
```

### 3. Portfolio Rebalancing
```
Monthly check:
- Sector allocation review
- Risk concentration check
- Rebalance to target weights
- Trim winners/add to losers
```

## Alert System

### Priority Levels
**🔴 CRITICAL:** Stop loss hit, major news
**🟡 WARNING:** Strategy signal, unusual volume
**🟢 INFO:** Daily report, position updates

### Telegram Integration
- Daily summary at 6 PM EST
- Critical alerts immediately
- Weekly report Sunday 9 PM EST
- On-demand portfolio check

## Data Management

### Sources
- Yahoo Finance API (free)
- Alpha Vantage (free tier)
- News RSS feeds
- Economic calendar

### Storage
- Portfolio history (CSV)
- Trade log (CSV)
- Performance metrics (JSON)
- Chart images (PNG)

### Backup
- Daily git commit of data
- Weekly archive to cloud
- Monthly full backup

## Tools & Skills Needed
1. **Market data fetcher** - Yahoo Finance/Alpha Vantage
2. **Technical indicators** - RSI, MACD, moving averages
3. **Portfolio tracker** - Holdings, P&L, performance
4. **News monitor** - RSS/API news aggregation
5. **Alert system** - Telegram integration
6. **Chart generator** - Simple performance charts
7. **Backtesting engine** - Strategy validation

## Success Checklist
- [ ] Daily reports automated
- [ ] Portfolio tracking accurate
- [ ] Alerts working reliably
- [ ] Strategies backtested
- [ ] Risk management implemented
- [ ] Visualization dashboard
- [ ] Performance vs benchmark tracking