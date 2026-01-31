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
**Projects (Work Type/State):**
1. **Tickets** — New work intake (inbox)
2. **Strategic** — Long-term optimization, R&D, system improvements
3. **Scheduled** — Time-bound, planned work with deadlines
4. **Backburner** — Low priority, blocked, future consideration
5. **Recurring** — Daily/weekly/monthly automated routines

**Labels (Ownership):**
- `@Clarke` — CEO-level strategic decisions
- `@Atlas` — PM-owned tasks (triaging, tracking, reporting)
- `@Forge` — Development, automation, technical work
- `@Ledger` — Finance, budgeting, transaction tracking

**Workflow:**
1. New task → **Tickets** project (no label yet)
2. **Atlas** triages → assigns owner label → moves to appropriate project
3. **Clarke** can assign directly to Atlas with label
4. Filter by label to see "all Forge's work" across projects

**Quick Commands:**
```bash
todoist today                    # Today's tasks
todoist tasks -p "Strategic"     # Project tasks
todoist add "Task name" --due "tomorrow" --priority 1 --label "@Forge"
todoist done <task-id>          # Complete task
```

**Automation:**
- `/root/clawd/scripts/todoist-auto-update.py` - Auto-sync with TASKS.json
- Can add tasks via chat: "add X to todoist"
- Morning brief includes today's tasks
- Automatic updates when work completes

**Current Tasks:**
- **Strategic:** 5 tasks (Mistral hybrid, Vector search, PostgreSQL, Redis, ROI report)
- **Scheduled:** 3 tasks (Smart home, Insurance shopping, Trading bot)
- **Backburner:** 3 tasks (Package tracking, Ultrahuman, Calendar)
- **Recurring:** 13 tasks (Window pings, backups, journals, reports)

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
