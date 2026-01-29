# Clarke's Finance Tracking System

**Built:** 2026-01-29  
**Version:** 1.0  
**Mandate:** Proactive evolution - Clarke implements improvements and informs Shirin

---

## Overview

Complete household finance tracking system with Telegram logging, automated summaries, and monthly PDF reports.

---

## Budget Summary

**Income (Monthly):**
- Shirin: $3,000 biweekly = $6,500/month
- Zeel: $3,200 biweekly = $6,933/month
- **Total:** $13,433/month

**Expenses (Monthly):**
- Fixed: $5,032
- Recurring: $1,886
- **Total:** $6,918/month

**Savings:**
- **Net Monthly:** $6,515
- **Savings Rate:** 48.5% 🔥

---

## Cycle

**27th to 27th** - All tracking and reports follow this cycle.

**Paydays:**
- Shirin: Biweekly from Jan 29th
- Zeel: Biweekly from Feb 6th

---

## How to Use

### Via Telegram (Easiest)

Just message Clarke naturally:

```
spent $45 grocery
zeel spent $120 eating out
paid $85 gas
```

Clarke will parse and log automatically.

### Via CLI

```bash
# Log a transaction
finance log 45.50 grocery "Costco run"
finance log 120 eating_out "Dinner downtown"

# View summaries
finance weekly      # Last 7 days
finance monthly     # Current 27-27 cycle
finance stats       # Quick stats

# Generate PDF
finance pdf         # Monthly report (27th-27th)

# View budget
finance budget

# Help
finance help
```

---

## Categories

- `grocery` - Groceries, Costco, food shopping
- `eating_out` - Restaurants, takeout, delivery
- `misc` - Miscellaneous household
- `gas` - Fuel for Tesla
- `shopping` - Clothing, Amazon, general shopping
- `gifts` - Gifts for friends/family
- `health` - Medical, pharmacy, wellness
- `entertainment` - Movies, events, hobbies
- `home` - Home improvements, furniture
- `auto` - Car maintenance, repairs
- `other` - Anything else

---

## Automated Reports

### Weekly Summary (Sundays 8 AM EST)
- Total spent last 7 days
- Breakdown by category
- Transaction count
- Delivered via Telegram

**Cron job:** `finance-weekly-summary`

### Monthly PDF Report (27th of each month, 9 AM EST)
- Full 27-27 cycle analysis
- Income vs expenses
- Actual vs budgeted spending
- Savings rate
- Category breakdown with detailed transactions
- Delivered via Telegram as PDF

**Cron job:** `finance-monthly-pdf`

---

## File Structure

```
/root/clawd/finance/
├── budget.json                    # Budget configuration
├── transactions/
│   ├── 2026-01.csv               # January transactions
│   ├── 2026-02.csv               # February transactions
│   └── ...
├── reports/
│   ├── finance-report-2026-01-27.md
│   ├── finance-report-2026-01-27.pdf
│   └── ...
└── README.md                      # This file
```

---

## Transaction Format (CSV)

```csv
date,amount,category,description,logged_by
2026-01-29 00:40:15,45.50,grocery,"Costco run",manual
2026-01-29 12:30:00,120.00,eating_out,"Lunch downtown",telegram
```

---

## Evolution & Improvements

**Clarke's mandate:** Proactively evolve this system and inform Shirin of changes.

**Planned improvements:**
- [ ] Automatic categorization (AI-based)
- [ ] Receipt photo parsing via Telegram
- [ ] Budget alerts (e.g., "Eating Out at 80% of budget")
- [ ] Spending trends analysis
- [ ] Savings goal tracking
- [ ] Export to Excel/Google Sheets

**Implemented changes will be logged here.**

---

## All State Insurance Reminder

**Current:** $550/month  
**Renewal:** April 2026  
**Action:** Shop for better rates in February

Clarke will remind you in February and provide comparison quotes.

---

## Quick Reference

### Log via Telegram
```
spent $45 grocery
```

### View weekly summary
```
finance weekly
```

### View monthly summary
```
finance monthly
```

### Generate PDF
```
finance pdf
```

### Check quick stats
```
finance stats
```

---

## Technical Details

**Scripts:**
- `/root/clawd/scripts/finance` - Main CLI
- `/root/clawd/scripts/finance-log.sh` - Transaction logger
- `/root/clawd/scripts/finance-report.py` - Summary generator
- `/root/clawd/scripts/finance-pdf.py` - PDF report generator

**Cron Jobs:**
- Weekly summary: Sundays 8 AM EST (`0 13 * * 0` UTC)
- Monthly PDF: 27th of month, 9 AM EST (`0 14 27 * *` UTC)

**Dependencies:**
- Python 3
- pandoc + texlive-xetex (for PDF generation)
- jq (JSON parsing)

---

## Support

Questions? Ask Clarke via Telegram. System will evolve based on usage patterns and needs.

---

*Built with care. Designed for visibility. Automated for convenience.*

— Clarke
