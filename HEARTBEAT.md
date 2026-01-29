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

## Memory System Usage (Every 3-4 hours during active work)
- Use the memory CLI tools we built:
  - `memory search <query>` - Search before asking Shirin repeated questions
  - `memory tag add memory/YYYY-MM-DD.md <tags>` - Tag important entries
  - `memory distill 7` - Weekly review (Sundays), suggest MEMORY.md updates
  - `memory stats` - Check memory file health
- Rule: ONE file per day. No fragments, no topic splits.
- Commit memory changes immediately after writing

## Self-Review (Every 3-4 hours during active work)
- Review last session block of work
- Ask myself:
  - What mistakes did I make?
  - What did I forget that I should have remembered?
  - Did I repeat a previous mistake?
  - Did I use the memory system properly?
- Document learnings in MEMORY.md under "## Lessons Learned"
- Track specific failure modes:
  - Timezone conversions (UTC ↔ EST)
  - Memory loss between sessions
  - Forgetting systems we built
  - Not using tools we created

## Improvement Analysis (Daily, before morning brief)
- Review today's memory file + recent conversations
- Identify friction points, inefficiencies, repeated manual work
- Generate 2-3 concrete improvement proposals
- Write to `/tmp/improvement-suggestions-YYYYMMDD.txt`:
  - Format: `• [Action] - [concrete benefit]`
  - Keep it brief: headline + one-line rationale
  - Focus on automation, token savings, time savings
- Morning brief will include these automatically at 5 AM EST
