# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.
# Add tasks below when you want the agent to check something periodically.

## Morning Check (once between 8-9 AM EST)
- If it's morning (8-9 AM EST) and I haven't sent a morning message today:
  - Say good morning
  - Remind to start a fresh session with `/new` for token efficiency
  - Ask if there's anything on the agenda for the day

## Overnight Autonomous Work (1-5 AM EST)
- If it's overnight (1-5 AM EST) and I haven't worked on autonomous tasks yet today:
  - Check `/root/clawd/TASKS.json` autonomous queue
  - Pick the highest priority incomplete task
  - Work on it for 30-90 minutes (make real progress)
  - Update progress in TASKS.json (%, milestones completed)
  - Commit changes to git with clear message
  - Write summary to `/tmp/overnight-work-YYYYMMDD.txt`:
    * What task I worked on
    * What got done (specific milestones/code/results)
    * Progress % or measurable outcome
    * Next steps
  - Morning brief will pick this up automatically at 6 AM
