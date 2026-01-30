# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.
# Add tasks below when you want the agent to check something periodically.

## When to Act vs Stay Silent
- **Act (respond with work/findings)** when:
  - Security alerts detected
  - System resources critically low
  - Autonomous work completed
  - Something needs Shirin's attention
  
- **Stay silent (HEARTBEAT_OK)** when:
  - All checks pass, nothing to report
  - Late night (11 PM - 7 AM) unless urgent
  - Last check was < 30 minutes ago

---

## Security Monitoring (Every 2-3 hours during day)
Check security logs and system health. Report if:
- Failed SSH login attempts > 50 in last 24h
- Unusual network activity detected
- Firewall rules changed
- New processes listening on ports

**Tools:**
- `/var/log/auth.log` - SSH attempts
- `ss -tlnp` - listening ports
- `/var/log/clarke-monitor/alerts.log` - automated alerts

**Action:** If threats found, summarize and alert. Otherwise, HEARTBEAT_OK.

---

## System Maintenance (Every 4-6 hours)
Check system resources and perform housekeeping:
- Disk usage > 80%?
- Memory usage > 85%?
- Log rotation needed?
- Stale temp files in `/tmp/`?

**Tools:**
- `df -h` - disk usage
- `free -h` - memory usage
- `/var/log/clarke-monitor/health.log` - monitoring data

**Action:** Auto-fix when safe (cleanup old logs, clear temp files). Report if manual intervention needed.

---

## Overnight Autonomous Work (1-5 AM EST)
When heartbeat runs during 1-5 AM window AND I haven't worked on autonomous tasks yet today:
1. Check `/root/clawd/TASKS.json` autonomous queue
2. Pick highest priority incomplete task
3. Work for 30-90 minutes (make real progress)
4. Update progress in TASKS.json (%, milestones)
5. Commit changes to git
6. Write summary to `/tmp/overnight-work-YYYYMMDD.txt`:
   - Task worked on
   - What got done (specific milestones/code/results)
   - Progress % or measurable outcome
   - Next steps

**Morning brief (5 AM) will pick this up automatically.**

---

## Memory System Review (Every 3-4 hours during active work)
Use memory CLI tools we built:
- `memory search <query>` - Before re-reading files
- `memory stats` - Check file health
- ONE file per day rule - merge if fragments exist

**Action:** Maintenance only (merge fragments, fix issues). Don't spam reports.

---

## Self-Review (Every 3-4 hours during active work)
Review last session block. Document in today's memory file:
- Mistakes made
- Things forgotten that should have been remembered
- Repeated mistakes
- Failure modes (timezone, memory loss, not using tools)

**Write to:** `memory/YYYY-MM-DD.md` under `## Self-Review`
**Track:** Timezone errors, memory loss, forgetting systems we built

**Action:** Write learnings, commit to git. Silent unless critical pattern found.

---

## Notes
- **Frequency:** Heartbeat polls every ~30 minutes (configurable)
- **Time-based checks:** Use CRON for exact timing, heartbeat for "every few hours"
- **Token efficiency:** Batch similar checks in one turn
- **Proactive work:** Can read/organize/commit without asking
