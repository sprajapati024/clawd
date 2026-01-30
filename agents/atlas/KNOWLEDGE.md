# Atlas Knowledge

## Todoist CLI Commands

**List tasks:**
```bash
todoist today                    # Today's tasks
todoist tasks -p "ProjectName"   # Project tasks
todoist tasks --filter "p1"      # Priority 1 tasks
todoist projects                  # List all projects
```

**Task operations:**
```bash
todoist done <task-id>                      # Mark complete
todoist comment <task-id> "progress update" # Add comment
todoist update <task-id> --priority 1       # Update priority
todoist view <task-id>                      # View details
todoist add "Task name" -p "Project" --priority 2  # Create task
```

**Search & filter:**
```bash
todoist search "keyword"         # Search tasks
todoist tasks --filter "overdue" # Overdue tasks
```

**NEVER use:**
- `todoist delete` - violates "never delete" policy
- Use `todoist done` instead

## Project Management Best Practices

- Status updates should be specific and actionable
- Flag blockers immediately with comments
- Track time estimates vs actuals
- Use priority levels (1=urgent, 2=high, 3=normal, 4=low)
- Add context in comments, not just "done"
- Comment format: `[Atlas YYYY-MM-DD HH:MM]: <update>`

## Project Structure (Clarke)

1. **Clarke - Autonomous Work** - Long-term optimization projects
2. **Clarke - Planned Tasks** - Scheduled upcoming work
3. **Clarke - Backburner** - Low priority / blocked items
4. **Clarke - Recurring Systems** - Daily/automated routines
