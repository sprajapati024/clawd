# Unified Morning Brief

**Schedule:** Every day at 6:00 AM EST (11:00 AM UTC)  
**Delivery:** Telegram  
**Purpose:** One comprehensive briefing to start your day

---

## What's Included

### ☀️ Good Morning Header
- Current date and day of week

### 🌤️ Weather - Toronto
- Current conditions (temperature, feels like, wind)
- Today's forecast
- Source: wttr.in (no API key needed)

### 🛡️ Overnight Security
- Status: secure or issues
- Failed login attempts blocked overnight
- Currently banned IPs
- Critical events auto-resolved (if any)

### 💚 System Health
- Disk usage
- Memory usage
- CPU load
- Uptime
- Service status (SSH, fail2ban, etc.)

### 💪 Your Health (Ultrahuman)
- Sleep score
- Readiness
- Activity summary
- *Currently pending API keys*

### 📆 Today's Schedule (Future)
- Calendar integration
- Upcoming meetings/events
- *Placeholder for when you share calendar access*

---

## Design Philosophy

**No context switching.** Everything you need in one message at 6 AM when you're at the gym:
- What happened overnight (security, system)
- What to expect today (weather, schedule)
- How you're doing (health metrics)

**Clean and scannable.** Emoji headers, sections separated, easy to read on mobile.

**Smart defaults.** If a service isn't configured yet (Ultrahuman, calendar), it says "pending" instead of failing.

---

## Scripts

**Main script:** `/root/clawd/scripts/morning-brief-unified.sh`  
**Latest copy:** `/var/log/clarke-monitor/latest-morning-brief.txt`  
**Cron job ID:** `8c2c3eaa-01d6-4fc2-9dcd-7ab60829c8d0`

### Manual Run
```bash
/root/clawd/scripts/morning-brief-unified.sh
```

---

## Cleanup Done

**Removed fragmented scripts:**
- ❌ `morning-brief.sh` (old)
- ❌ `morning-brief-full.sh` (old)
- ❌ `write-journal.sh` (unused)
- ❌ `send-journal.sh` (unused)
- ❌ `send-security-report.sh` (redundant)

**Result:** Clean `/scripts/` directory with only active, necessary scripts.

---

## Future Enhancements

- [ ] Calendar integration (when you share access)
- [ ] Ultrahuman health data (when API keys provided)
- [ ] Traffic/commute info (if relevant)
- [ ] Coffee's birthday reminders :)
- [ ] Weekly goals/habits tracking

---

## Test Output (2026-01-28)

```
☀️ GOOD MORNING
📅 Wednesday, January 28, 2026

🌤️ WEATHER - Toronto
Partly cloudy -9°C | Feels like: -16°C | Wind: →18km/h

🛡️ OVERNIGHT SECURITY
Status: ✅ All systems secure
Failed attempts blocked: 0
IPs currently banned: 0

💚 SYSTEM HEALTH
💾 Disk: 42%
🧠 Memory: 13%
⚙️ CPU Load: 0.32
⏱️ Uptime: 1 hour, 49 minutes
✅ All services running

💪 YOUR HEALTH
⏳ Ultrahuman integration pending (need API keys)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Have a good day. I'll be here if you need me.
— Clarke
```

**✅ All tests passed. Ready for production.**

---

*One message. Everything you need. No fragments.*

— Clarke
