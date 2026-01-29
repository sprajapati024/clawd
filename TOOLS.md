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
