# 📝 Memory Writing Checklist - Write IMMEDIATELY

**The rule:** After EVERY significant action, write to memory BEFORE replying.

## What Triggers Memory Writing (Mandatory)

### 🛠️ Build/Create Actions
- [ ] Created new file/script/system
- [ ] Built new feature/tool
- [ ] Configured new service/API
- [ ] Generated code
- [ ] Modified architecture

**Write:** What was built, why, how it works, where it lives

### 🔧 Configuration Changes
- [ ] Modified config files
- [ ] Changed system settings
- [ ] Updated environment variables
- [ ] Added/removed cron jobs
- [ ] Changed permissions/security

**Write:** What changed, why, impact, rollback info if needed

### 📚 Learning/Discovery
- [ ] Researched something new
- [ ] Found solution to problem
- [ ] Discovered how something works
- [ ] Read documentation that matters
- [ ] Learned from mistake

**Write:** What was learned, source, how to apply it

### ✅ Task Completion
- [ ] Finished major task
- [ ] Shipped feature
- [ ] Solved problem
- [ ] Fixed bug
- [ ] Completed milestone

**Write:** What was done, outcome, next steps

### 💡 Decisions Made
- [ ] Chose approach A over B
- [ ] Set priority/direction
- [ ] Made architectural choice
- [ ] Rejected an option
- [ ] Changed strategy

**Write:** Decision, rationale, alternatives considered

### ❌ Mistakes/Failures
- [ ] Something broke
- [ ] Made error in judgment
- [ ] Forgot something important
- [ ] Repeated past mistake
- [ ] Misunderstood requirement

**Write:** What went wrong, why, how to prevent next time

### 📅 Schedule/Time-Sensitive
- [ ] Set reminder/cron job
- [ ] Scheduled work for later
- [ ] Created deadline
- [ ] Committed to timeline
- [ ] Postponed something

**Write:** What, when, why, where to find it

---

## The Pattern (MANDATORY)

```bash
1. Do the significant action
2. IMMEDIATELY write to memory/YYYY-MM-DD.md
3. IMMEDIATELY run: bash /root/clawd/scripts/memory-auto-commit.sh
4. THEN reply to user
```

**Never:** 
❌ Say "I'll document this later"
❌ Batch multiple changes before writing
❌ Reply first, write later
❌ Take "mental notes" (they don't persist)

**Always:**
✅ Write immediately (while context is fresh)
✅ Commit immediately (so it persists)
✅ Be specific (exact commands, paths, outcomes)
✅ Include tags for searchability

---

## Memory File Structure (Today's File)

```markdown
# Memory - YYYY-MM-DD

## [Task/Event Name] (HH:MM UTC / HH:MM AM/PM EST)

**Context:** Why this happened

**What I did:**
1. Step one
2. Step two
3. Step three

**Outcome:** What resulted

**Files changed:**
- path/to/file.ext (what changed)

**Commands used:**
```bash
exact commands here
```

**Lessons learned:**
- Specific takeaway
- What to do differently next time

**Git commit:** abc1234 (if applicable)

---

#tags #for #searching
```

---

## Quick Reference

**Built something?** → Write it now
**Changed config?** → Write it now
**Learned something?** → Write it now
**Made decision?** → Write it now
**Made mistake?** → Write it now
**Scheduled something?** → Write it now

**THEN commit:**
```bash
bash /root/clawd/scripts/memory-auto-commit.sh
```

**No exceptions. No delays. No batching.**
