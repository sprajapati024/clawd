# TOOLS.md - Local Notes

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Todoist Integration

**API Token:** Configured ✅
**Projects:**
- `Clarke - Autonomous Work` - Long-term optimization projects
- `Clarke - Planned Tasks` - Scheduled upcoming work
- `Clarke - Backburner` - Low priority / blocked tasks
- `Clarke - Recurring Systems` - Daily/automated routines

**Quick Commands:**
```bash
todoist today                    # Today's tasks
todoist tasks -p "Clarke - Autonomous Work"  # Project tasks
todoist add "Task name" --due "tomorrow" --priority 1
todoist done <task-id>          # Complete task
```

**Automation:**
- `/root/clawd/scripts/todoist-auto-update.py` - Auto-sync with TASKS.json
- Can add tasks via chat: "add X to todoist"
- Morning brief includes today's tasks
- Automatic updates when work completes

**All migrated from TASKS.json:**
✅ 4 autonomous projects (Mistral hybrid, Vector search, PostgreSQL, Redis)
✅ 2 planned tasks (Smart home, Insurance shopping)  
✅ 3 backburner items (Package tracking, Ultrahuman, Calendar)
✅ 7 recurring systems (VPS monitoring, security, backups, trading bot)

## Timezone
- **Shirin's timezone:** EST/EDT (Toronto)
- **System time:** UTC
- **Offset:** UTC -5 (EST) / UTC -4 (EDT during daylight saving)
- **Always convert UTC to EST/EDT when talking about time**

## Trading Bot Commands

**Portfolio Review:**
```bash
cd /root/clawd/projects/day-trader && python3 scripts/portfolio_review.py
```
Alias: `/portfolio` (via Telegram)

**Schedule:**
- Runs Mon-Fri at 4:30 PM EST (automated via cron)
- Daily report sent to Telegram after market close
- Shows: holdings, P&L, trades, closing balance

**Files:**
- Portfolio: `/root/clawd/projects/day-trader/portfolio.csv`
- Trades: `/root/clawd/projects/day-trader/trades.csv`
- Reports: `/root/clawd/projects/day-trader/logs/report_*.txt`

**API Keys Needed:**
- DeepSeek API (OpenRouter) - for trading decisions
- Financial Datasets API (optional) - for real market data
- Tavily API (optional) - for news/research

## VPS Monitoring Setup

**Monitoring runs every 5 minutes via cron**

Logs:
- `/var/log/clarke-monitor/alerts.log` — critical alerts (disk full, memory spike, service down)
- `/var/log/clarke-monitor/health.log` — regular health snapshots

Thresholds (automatic alerts):
- **Disk:** >80% usage
- **Memory:** >85% usage
- **CPU:** >90% load average
- **SSH:** >50 failed login attempts
- **Clawdbot:** process check

Tools installed:
- **imagemagick** — image processing (resize, convert, optimize)
- **jq** — JSON parsing/manipulation
- **sysstat** — performance analysis
- **htop** — interactive process monitor
- **nethogs** — network usage by process

## How I'll Help

- Daily health check during heartbeats
- Alert you if thresholds are hit
- Auto-restart services if they die
- Suggest fixes (disk cleanup, memory optimization)
- Never let something be broken without you knowing

---

## Next Setup

- ffmpeg (hold for now — need specific use case)
- Automated backups (when you're ready)
- Custom Telegram alerts (integrate with bot)

## ClawdHub Skills Installed (Jan 30, 2026)

**VPS-compatible skills only** (macOS/iOS skills removed - no Mac Mini)

**Stock & Finance:**
- dexter - Stock research agent (needs API keys)

**Task Management:**
- todoist - Task management (needs API token)

**Google Workspace:**
- google-workspace-mcp - Google Workspace MCP
- gog - Google Workspace CLI (needs OAuth)

**Development & Deployment:**
- vercel - Deploy CLI

**Utilities:**
- track17 - Package tracking
- youtube-summarizer - Video transcripts
- steam - Steam Deck library

**API Keys Needed:**
1. Dexter: Financial Datasets + Tavily API keys
2. Todoist: API token + CLI installation
3. Google Workspace: OAuth credentials

**Next Actions:**
1. Configure API keys for priority skills
2. Test basic functionality of installed skills
