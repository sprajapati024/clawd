# Daily Security Report

**Schedule:** Every day at 10:00 AM EST (3:00 PM UTC)  
**Delivery:** Telegram  
**Purpose:** Educational security briefing

## What's Included

### 📊 Threat Summary
- Failed login attempts (past 24h)
- Currently banned IPs
- Lifetime total bans
- Root login attempts

### 🚨 New Bans
- List of IPs banned in past 24h
- Timestamps
- Geographic location (if available)

### 🎯 Attack Patterns
- Most targeted usernames
- Attack timing (hourly distribution)
- Identifies patterns in attacker behavior

### 🔧 Auto-Healing Actions
- Services restarted automatically
- Problems fixed without intervention
- System self-maintenance log

### 💚 Current System Status
- Disk usage
- Memory usage
- CPU load
- Firewall status
- fail2ban status

### 📚 Learning Section
**This is the key part!** Contextual explanations that teach you:
- What each type of attack means
- Why certain patterns happen
- How our defenses work
- What's normal vs. concerning

## Examples of What You'll Learn

**High Failed Login Activity:**
> Your server is being scanned by automated bots trying common
> usernames and passwords. This is NORMAL for any public server.
> Our system blocks them after 3 attempts for 24 hours.

**Root Login Attempts:**
> Attackers always try "root" first because it exists on every Linux
> system. We've disabled root password login entirely - they can't
> get in even if they guess the password.

**Multiple Banned IPs:**
> This could indicate coordinated attack or normal background noise.
> fail2ban automatically bans after repeated failures.

## Script Locations

- Report generator: `/root/clawd/scripts/security-daily-report.sh`
- Latest report: `/var/log/clarke-monitor/latest-security-report.txt`
- Send log: `/var/log/clarke-monitor/report-sends.log`

## Manual Run

To see the report anytime:
```bash
/root/clawd/scripts/security-daily-report.sh
```

## Cron Job

Set up via Clawdbot cron system:
- **Label:** "Daily Security Report (10 AM EST)"
- **Schedule:** 0 15 * * * (3 PM UTC = 10 AM EST)
- **Delivery:** Direct to your Telegram

---

**Goal:** You learn about threats as they happen, understand how the system protects you, and build security intuition over time.

— Clarke
