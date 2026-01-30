# TOOLS.md - Local Notes

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Timezone
- **Shirin's timezone:** EST/EDT (Toronto)
- **System time:** UTC
- **Offset:** UTC -5 (EST) / UTC -4 (EDT during daylight saving)
- **Always convert UTC to EST/EDT when talking about time**

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

**Stock & Finance:**
- dexter - Stock research agent (needs API keys)

**Task Management:**
- todoist - Task management (needs API token)
- things-mac - Things 3 CLI (macOS)

**Google Workspace:**
- google-workspace-mcp - Google Workspace MCP
- gog - Google Workspace CLI (needs OAuth)

**Apple Ecosystem:**
- apple-remind-me - Natural language reminders (macOS)
- apple-contacts - Contact lookup (macOS)
- apple-photos - Photo search (macOS)
- apple-music - Music control (macOS)
- apple-mail-search - Fast Mail search (macOS)
- healthkit-sync - Gym data sync (iOS/macOS)
- icloud-findmy - Device tracking (iCloud)
- shortcuts-skill - iOS/macOS automation

**Development & Deployment:**
- vercel - Deploy CLI

**Utilities:**
- track17 - Package tracking
- youtube-summarizer - Video transcripts
- steam - Steam Deck library

**iMessage Options:**
- BlueBubbles: Requires Mac Mini (recommended)
- Pypush: Experimental, high risk
- Beeper: Subscription service
- See /tmp/imessage-setup-guide.txt for details

**API Keys Needed:**
1. Dexter: Financial Datasets + Tavily API keys
2. Todoist: API token + CLI installation
3. Google Workspace: OAuth credentials
4. Apple ecosystem: macOS environment

**Next Actions:**
1. Configure API keys for priority skills
2. Consider Mac Mini for Apple ecosystem integration
3. Test basic functionality of installed skills
