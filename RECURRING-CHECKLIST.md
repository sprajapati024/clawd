# RECURRING SYSTEMS CHECKLIST

**Purpose:** Track automated systems that run via cron/scheduled jobs. These don't need active Todoist tasks since they're automated.

## ✅ Active Systems

### 1. VPS Monitoring
- **Schedule:** Every 5 minutes via cron
- **Checks:** Disk, memory, CPU, SSH attempts, services
- **Alerts:** `/var/log/clarke-monitor/alerts.log`
- **Status:** ✅ Active

### 2. Security Audit  
- **Schedule:** Daily at 9:03 AM EST
- **Checks:** Failed logins, open ports, firewall changes
- **Alerts:** Auto-report if threats detected
- **Status:** ✅ Active

### 3. Trading Bot Daily Routine
- **Schedule:** Mon-Fri at 4:30 PM EST (after market close)
- **Actions:** Portfolio review, trading decisions, reporting
- **Output:** Telegram report with trades + P&L
- **Status:** ✅ Active (mock data), ⏸️ Waiting on API keys

### 4. Auto-heal Services
- **Schedule:** Every 15 minutes via cron
- **Checks:** Clawdbot, monitoring services, critical processes
- **Actions:** Auto-restart if dead, alert if persistent
- **Status:** ✅ Active

### 5. Predictive Monitoring
- **Schedule:** Every 30 minutes via cron
- **Checks:** Trend analysis, anomaly detection
- **Actions:** Early warning for resource trends
- **Status:** ✅ Active

### 6. Automated Backups
- **Schedule:** Daily at 2:00 AM EST
- **Scope:** `/root/clawd/` workspace, configs, memory files
- **Storage:** Git commits + optional cloud sync
- **Status:** ✅ Active

### 7. Git Backup
- **Schedule:** After every significant change
- **Trigger:** Memory auto-commit script
- **Scope:** All workspace changes
- **Status:** ✅ Active

## 📊 Health Dashboard
Check during heartbeats (every 2-3 hours):
- `df -h` - Disk usage (>80% = alert)
- `free -h` - Memory usage (>85% = alert)
- `/var/log/clarke-monitor/alerts.log` - Critical issues
- Service status (Clawdbot, monitoring scripts)

## 🔧 Maintenance Notes
- **Log rotation:** Weekly cleanup of old logs
- **Temp cleanup:** Daily `/tmp/` cleanup
- **Updates:** Security patches as needed
- **Backup verification:** Monthly restore test

---

**Last updated:** 2026-01-30 09:27 EST  
**Next review:** During next heartbeat (check for alerts only)