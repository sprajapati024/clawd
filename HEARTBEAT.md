# HEARTBEAT.md

# 🔄 HEARTBEAT v2 (Every 45 minutes)

## Meta
- **Frequency:** Every **45 minutes** (best‑effort, may drift a few minutes)
- **24/7 operation:** Heartbeat runs continuously, day and night
- **Goal:** Shirin never has to ask “?” — status is always visible, automation is transparent

## Report Structure
```
**Heartbeat [TIME EST]**
- ✅ System: [Health summary]
- ⚠️ Team: [Blockers / decisions needed]
- 🚦 Dispatcher: [Todoist actions taken]
- 🔄 Active work: [Agents currently running]

**Action needed:** [None / Clarify X / Review Y]
```

If nothing happened:
```
**Heartbeat [TIME EST]**
- ✅ System healthy
- ✅ No tasks eligible
```

---

## 1️⃣ System & Security (Exception‑only reporting)
**Why:** You don’t want surprises.

### Checks:
- Disk usage (alert if >80%)
- Memory usage (alert if >85%)
- CPU load (alert if >90%)
- Clawdbot service status
- Failed SSH attempts (last 24h)
- `/var/log/clarke-monitor/alerts.log` (automated alerts)

### Tools:
- `df -h`, `free -h`, `uptime`
- `systemctl status clawdbot`
- `/var/log/auth.log`
- `sudo fail2ban-client status`

### Report format:
- ✅ System: Healthy
- ⚠️ System: Disk 82% (cleanup needed)
- 🔴 System: Service down [details]

---

## 2️⃣ Team Status (CEO‑level oversight)
**Why:** Visibility, not micromanagement.

### Checks:
- **Atlas:** Blockers, decisions needed, priority conflicts
- **Forge:** Active work, technical blockers
- **Ledger:** Anomalies, reporting schedule

### Delegation model:
- Specialists own domain details
- Clarke (CEO) gets summary reports
- Escalate only blockers, conflicts, or decisions needing approval

### Report format:
- ⚠️ Team: Atlas blocked on X
- ✅ Team: All clear

---

## 3️⃣ 🚦 Todoist DISPATCHER (NEW — CORE)
**This is the due‑time execution engine you designed.**

### What it checks (every heartbeat)
All tasks that:
- Are assigned
- Are **NOT**:
  - `Status: Done`
  - `Status: In progress`
  - `Status: Blocked`

### Due‑time gate (non‑negotiable)
- If **now < due time** → ignore
- If **now ≥ due time** → eligible

### Action (INLINE, for ALL eligible tasks)
For each eligible task:

- 🟡 **Status: Needs clarity**
  - Ask Shirin the pending question (once)

- 🟢 **Status: Ready**
  - Nudge assigned owner **or**
  - Start agent (when appropriate)

### Guardrails
- ✅ Never start early
- ✅ Never assume if unclear
- ✅ One active task per owner at a time
- ✅ Late night (11 PM–7 AM) → defer unless marked urgent

### Report format:
- 🚦 Dispatcher:
  - Task A → nudged Forge
  - Task B → asked Shirin for clarity
- ✅ No tasks eligible

---

## 4️⃣ Active Work (Motion, not inventory)
**Why:** You care about what’s moving.

### Checks:
- Which agents are currently active
- What they’re working on
- Any blockers

### Report format:
- 🔄 Active work: Forge on Fitness Trainer
- ✅ No active work

---

## 5️⃣ Memory Discipline (Silent unless wrong)
**Why:** Keeps Clarke honest.

### Checks:
- Memory written after significant actions
- Fragmentation (multiple files per day)
- Session freshness (context %, age, compactions)

### Tools:
- `bash /root/clawd/scripts/memory-check.sh`
- `📊 session_status`

### Report format:
- ✅ Memory: Recent commits, single file per day
- ⚠️ Memory: Fragmentation detected, needs merge
- 🔴 Memory: No recent commits, slipping discipline

---

## 6️⃣ Self‑Review (MANDATORY — internal only)
**Why:** Continuous improvement.

### Questions (answer in `memory/YYYY‑MM‑DD.md` under `## Self‑Review`):
1. Did I write to memory immediately after significant actions?
2. Did I forget something I should have remembered?
3. Any timezone errors or memory loss?
4. Did I suggest `/new` when appropriate?

**Action:** Write self‑review, commit changes, report only if slipping.

---

## What we REMOVE (intentional noise reduction)
❌ Detailed Todoist task lists  
❌ Commit‑by‑commit git reporting  
❌ Repeated “all clear” verbosity  
❌ Overnight autonomous work (not yet active)  
❌ TASKS.json progress (unless actively used)

---

## Implementation Notes
- **Always report:** No more “HEARTBEAT_OK” or witty one‑liners
- **Structure:** Use the report format above consistently
- **24/7 operation:** Heartbeat runs continuously, day and night
- **Goal:** Shirin never has to ask “?” — status is always visible
