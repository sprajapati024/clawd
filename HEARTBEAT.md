# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.
# Add tasks below when you want the agent to check something periodically.

## Proactive Status Reporting (Every 30 minutes)
**NEVER respond with "HEARTBEAT_OK" or witty one-liners.** Always provide a status report.

### Report structure:
```
**Heartbeat [TIME EST]**
- ✅ [What's working]
- ⚠️ [What's blocked/needs attention]
- 📋 [What's next]
- 🔄 [Active sub-agents]
- 📊 [System health]

**Action needed:** [None / Review X / Decision on Y]
```

### What to check (every heartbeat):
1. **Team status (Atlas, Forge, Ledger)** - Progress, blockers, ETA
2. **System health** - VPS monitoring alerts (disk, memory, CPU, security)
3. **Autonomous work** - Progress on TASKS.json items
4. **Memory discipline** - Recent commits, fragmentation, session freshness
5. **Anything needing Shirin's attention** - Decisions, reviews, approvals

**Note:** Todoist tasks are Atlas's responsibility. Atlas reports PM status to Clarke, Clarke synthesizes for Shirin.

### Late night exception (11 PM - 7 AM EST):
- Only report if urgent (security, system down)
- Otherwise: "Night shift quiet. Systems stable."

### Why this matters:
- Shirin shouldn't have to ask "?"
- Surface blockers before they become problems
- Show momentum, not just "all quiet"

---

## Security Monitoring (Every heartbeat)
Check security logs and system health. **Always report status.**

**Checks:**
- Failed SSH login attempts (last 24h)
- Unusual network activity
- Firewall rule changes
- New processes listening on ports
- `/var/log/clarke-monitor/alerts.log` - automated alerts

**Tools:**
- `/root/clawd/scripts/security-monitor.sh` - Automated security check
- `/var/log/auth.log` - SSH attempts
- `ss -tlnp` - listening ports
- `sudo fail2ban-client status` - banned IPs

**Report format:**
- ✅ Security: No threats detected
- ⚠️ Security: [X] failed SSH attempts in 24h
- 🔴 Security: [Critical alert details]

---

## System Health (Every heartbeat)
Check system resources. **Always report status.**

**Checks:**
- Disk usage (alert if >80%)
- Memory usage (alert if >85%)
- CPU load (alert if >90%)
- Service status (Clawdbot, monitoring)
- Log health (rotation needed?)

**Tools:**
- `df -h` - disk usage
- `free -h` - memory usage
- `uptime` - CPU load
- `systemctl status clawdbot` - service check
- `/var/log/clarke-monitor/health.log` - monitoring data

**Report format:**
- ✅ System: Disk 45%, Memory 60%, CPU 12%
- ⚠️ System: Disk 82% (cleanup needed)
- 🔴 System: Service down [details]

---

## Active Work Tracking (Every heartbeat)
Check all active work and report progress.

**What to check:**
1. **Sub-agents** - Status, progress, blockers
2. **Todoist tasks** - Overdue, completed, upcoming
3. **TASKS.json autonomous queue** - Progress, next steps
4. **Git commits** - Recent changes, uncommitted work

**Report format:**
- 👔 Team: Atlas tracking 4 tasks (2 done today), Forge ready, Ledger standby
- 🔄 Sub-agents: [any active background work]
- 📋 TASKS.json: "Mistral hybrid" 40% complete
- 📝 Git: Last commit 2h ago, no uncommitted changes

**Overnight work (1-5 AM EST):**
If in window AND haven't worked on autonomous tasks today:
1. Pick highest priority task from TASKS.json
2. Work 30-90 minutes
3. Update progress
4. Commit changes
5. Report in next heartbeat

## Team Coordination (Every heartbeat)
CEO-level oversight of specialist agents.

**Atlas (PM Agent) - Check:**
1. Are tasks being tracked properly?
2. Any blocked tasks needing escalation?
3. Priority conflicts or resource allocation issues?
4. Ask Atlas for summary: "What's the PM status?"

**Forge (Developer Agent) - Check:**
1. Any active build/automation work?
2. Technical blockers needing CEO decision?
3. Performance or quality issues?

**Ledger (Finance Agent) - Check:**
1. Transaction categorization running smoothly?
2. Budget alerts or anomalies?
3. Financial reporting on schedule?

**Delegation model:**
- Specialists own their domain details
- Clarke (CEO) gets summary reports
- Escalate only blockers, conflicts, or decisions needing approval

**Example report:**
- 👔 Atlas: 4 tasks tracked, 2 completed today, 1 blocked (needs API key)
- 🔨 Forge: No active builds, ready for work
- 💰 Ledger: Not yet deployed (awaiting transaction data)

---

## Memory System Review (Every heartbeat)
**MANDATORY:** Check memory capture discipline and system health.

**What to check:**
1. **Memory writing discipline** - Did I write immediately after significant actions?
2. **Recent commits** - Are memory changes being committed?
3. **File fragmentation** - Multiple memory files for same day?
4. **Session freshness** - Context usage, age, compactions
5. **Self-review** - Mistakes, forgotten items, failure modes

**Checks to run:**
```bash
bash /root/clawd/scripts/memory-check.sh
📊 session_status
```

**Report format:**
- ✅ Memory: Recent commits, single file per day
- ⚠️ Memory: Fragmentation detected, needs merge
- 🔴 Memory: No recent commits, slipping discipline
- 📊 Session: Context X%, Age Xh, Compactions X

**Self-review questions (answer in memory file):**
1. Did I write to memory immediately after significant actions?
2. Did I forget something I should have remembered?
3. Any timezone errors or memory loss?
4. Did I suggest /new when appropriate?

**Action:** Write self-review to `memory/YYYY-MM-DD.md` under `## Self-Review`, commit changes. Report status in heartbeat.

---

## Memory Capture Discipline (Every heartbeat)
**Goal:** Never let things slip through the cracks.

**Triggers - Write memory NOW when you:**
- Build/create/configure something
- Make a decision or choose an approach
- Learn something new or solve a problem
- Complete a task or reach milestone
- Make a mistake or encounter failure
- Schedule/postpone work

**Pattern:** Do → Write → Commit → Reply (in that order)

**Checklist:**
- ✅ Memory file exists for today
- ✅ Recent changes committed (last 30 minutes)
- ✅ No fragmentation (only one file per day)
- ✅ Self-review section updated
- ✅ Session freshness monitored

**Reference:** See `/root/clawd/docs/CHECKLIST-memory-writing.md` for full checklist

---

## Implementation Notes
- **Frequency:** Heartbeat polls every ~30 minutes (configurable)
- **Always report:** No more "HEARTBEAT_OK" or witty one-liners
- **Structure:** Use the report format above consistently
- **Late night:** Only urgent reports 11 PM - 7 AM EST
- **Goal:** Shirin never has to ask "?" — status is always visible
