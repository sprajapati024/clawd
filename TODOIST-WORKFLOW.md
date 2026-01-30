# TODOIST WORKFLOW - MANDATORY

**From now on: EVERYTHING goes to Todoist with comments.**

## When to Add Tasks

**Immediately add to Todoist when:**
- Shirin asks me to do something
- I start working on something proactively
- I discover a task that needs doing
- Sub-agent creates work items
- New automation/cron job added
- Bug found that needs fixing
- Idea suggested for future work

## Required Information

**Every task must have:**
1. **Clear title** - What needs to be done
2. **Project** - Which Clarke project (Autonomous/Planned/Backburner/Recurring)
3. **Due date** (if applicable) - When it should be done
4. **Priority** - 1 (urgent), 2 (important), 3 (normal), 4 (low)
5. **Initial comment** - Context, details, plan, blockers

## Comment Updates

**Add comments when:**
- Work starts ("Starting work on X...")
- Progress made ("Completed milestone: Y")
- Blockers encountered ("Blocked by: Z")
- Work completed ("Finished! Outcome: ...")
- Status changes ("On hold for API keys")

## Projects

**Clarke - Autonomous Work**
- Long-term optimization projects
- Infrastructure improvements
- Things I work on during downtime

**Clarke - Planned Tasks**
- Scheduled work with specific dates
- Things Shirin asked for
- Time-sensitive items

**Clarke - Backburner**
- Low priority items
- Blocked/waiting tasks
- "Nice to have" features

**Clarke - Recurring Systems**
- Daily/automated routines
- Cron jobs
- Monitoring tasks

## Example Workflow

```bash
# Shirin asks: "Build a finance tracker"
todoist add "Finance Tracker - Build expense logging system" \
  --project "Clarke - Planned Tasks" \
  --priority 1 \
  --due "tomorrow"

# Add initial comment
todoist comment <task-id> "Requirements: Telegram logging, weekly summaries, monthly PDF. Tech: Python + SQLite. Estimated: 3-4 hours."

# During work
todoist comment <task-id> "Started work at 10:00 AM. Database schema created."

# Progress update
todoist comment <task-id> "Telegram logging complete. Testing weekly summary generation."

# Completion
todoist comment <task-id> "Completed! Live and tested. Files: /root/clawd/finance/*.py"
todoist done <task-id>
```

## Quick Commands

```bash
# List today's tasks
todoist today

# Add task
todoist add "Task name" -p "Project" --priority N --due "date"

# Add comment
todoist comment <id> "Comment text"

# Complete task
todoist done <id>

# View task details
todoist view <id>
```

## Integration Points

**Morning Brief:**
- Show today's high-priority tasks
- Mention upcoming deadlines

**Heartbeats:**
- Check for overdue tasks
- Update progress on active work

**Sub-agents:**
- Create Todoist task for each spawned job
- Update with results when complete

**Memory:**
- Reference Todoist task IDs in memory entries
- Link tasks to completed work

## Verification Checklist

Before replying to Shirin:
- [ ] Did I add the task to Todoist?
- [ ] Did I choose the right project?
- [ ] Did I add an initial comment with context?
- [ ] Did I set appropriate priority/due date?
- [ ] Is the title clear and actionable?

**No exceptions. If Shirin asks for something, it goes to Todoist FIRST, then I do it.**
