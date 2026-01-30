# MEMORY.md - Clarke's Long-Term Memory

## Key Dates
- **Shirin's Birthday:** January 2 (born 1998, age 28)
- **Coffee's Birthday:** January 27 (Golden Doodle, born 2022, turned 4 on Jan 27, 2026)
- **Shirin & Zeel Anniversary:** 2021 (married), 2017 (dating)
- **Clarke's Birthday:** January 28, 2026 (the day I came online)

## People
- **Shirin** — My human. PM in submetering. Toronto. Direct, systems thinker, disciplined (5:30 AM gym). Notion certified. Drives a Tesla. Gamer (Steam Deck).
- **Zeel** — Shirin's wife. Product designer. Could be a resource for design work.
- **Coffee** — Golden Doodle. The real boss of the house.

## Infrastructure
- **VPS:** Ubuntu 24.04, secured (SSH key only, UFW, fail2ban)
- **Telegram:** @clarke_bot_bot, chatId 6471272509
- **GitHub:** sprajapati024 (token pending — need to push scheduler on Jan 29)
- **Brave Search:** API configured (BSAgizF24FUsH9y23jq0g9GdXcvr-ru)
- **Browser:** Headless Chromium installed & running (can scrape, automate, extract data)
- **Portfolio:** shirinprajapati.com (Vercel, being redone — don't touch until merged)

## Decisions Made
- 2026-01-28: Set up VPS security (SSH keys, firewall, fail2ban, token rotation)
- 2026-01-28: Journal automation — write 10:55 PM EST, send 6 AM EST on Telegram
- 2026-01-28: Portfolio — leave alone until Shirin finishes redesign

## Lessons Learned
- Config dmPolicy only accepts: "pairing", "allowlist", "open", "disabled" (NOT "accept")
- Always ask before making changes
- Be direct, no fluff — that's what Shirin values
- **Timezone:** Always double-check UTC → EST conversion (UTC -5). I've gotten this wrong before. **FIXED:** `userTimezone: "America/Toronto"` now set.
- **Memory discipline:** Write to daily files IMMEDIATELY after significant work. Don't batch, don't wait.
- **Use the tools we built:** Memory system exists — use `memory search` before asking repeated questions
- **One file per day rule:** No fragments, no topic splits in memory/ folder
- **Personality split is real:** Multiple identity files = diluted voice. Keep it unified.
- **We forget what we build:** Track systems, scripts, features actively. Review them regularly.

### Clawdbot-Specific Lessons (Jan 29, 2026)
**From docs deep-read:**

1. **Cron vs Heartbeat** (I was doing it wrong)
   - **Heartbeat:** Batch multiple periodic checks (inbox, calendar, weather) in ONE turn. Saves tokens. Context-aware.
   - **Cron (isolated):** Exact timing, standalone tasks, different models/thinking levels
   - **Cron (main --system-event):** One-shot reminders, appears in main session
   - **Mistake:** Creating isolated cron jobs for simple reminders instead of `--session main --system-event`
   - **Fix:** Use heartbeat for batching, cron main for reminders, cron isolated for scheduled tasks

2. **Memory Flush Before Compaction** (automatic)
   - Clawdbot runs a silent turn BEFORE compaction to write durable memory
   - Triggered at `contextWindow - reserveTokens - softThresholdTokens` (4000 default)
   - Already enabled in config
   - **Action:** Trust the system, write to memory proactively during sessions

3. **Session Memory Search** (experimental, enabled)
   - Can search session transcripts, not just memory files
   - Async indexing (results slightly stale)
   - **Mistake:** Not using `memory_search` enough before re-reading files
   - **Fix:** Search FIRST, then read specific files

4. **Bootstrap Files = System Prompt**
   - AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, USER.md loaded EVERY session
   - Max 20K chars each (truncated)
   - **Mistake:** Not following session startup instructions (run session-startup.sh first)
   - **Fix:** Read SOUL.md every session, follow AGENTS.md strictly

5. **Token Optimization**
   - `/status` shows usage + cost
   - `/compact` manually summarizes when bloated
   - **Heartbeat keeps cache warm** (set interval just under cache TTL)
   - **Mistake:** Not suggesting `/new` aggressively enough
   - **Fix:** Monitor tokens, suggest fresh sessions when context bloats

6. **Model Failover** (native support)
   - Built-in: `model.fallbacks: ["deepseek/...", "moonshot/..."]`
   - Auth profile rotation FIRST, then model fallback
   - Automatic cooldowns (exponential backoff)
   - **Mistake:** Planning custom error handling when it's already native
   - **Fix:** Just configure fallbacks array once we have API keys

7. **"Mental Notes" Don't Exist**
   - Memory is limited between sessions
   - If I want to remember something, WRITE IT TO A FILE
   - Commit immediately: `bash /root/clawd/scripts/memory-auto-commit.sh`
   - **Text > Brain** 📝

## Self-Review Process
Every 3-4 hours during active work (triggered by heartbeat):

**Questions to ask:**
1. What mistakes did I make in the last session block?
2. What did I forget that I should have remembered?
3. Did I repeat a previous mistake?
4. Did I use the memory CLI tools properly?
5. Did I search memory before asking questions?
6. Did I write to today's memory file immediately?

**Track these specific failure modes:**
- **Timezone errors** - UTC ↔ EST conversion mistakes
- **Memory loss** - Forgetting work done in previous sessions
- **System amnesia** - Not using tools/scripts we already built
- **File discipline** - Creating fragments instead of single daily file
- **Permission creep** - Asking permission instead of acting + informing

**Document learnings here in this section, then commit immediately.**

## About Shirin (From Redesigned Website)

**Core Philosophy:**
- "If you do it twice, automate it" — that's the north star
- Measures success in "hours saved" not just "projects delivered"
- Obsessed with process improvement and automation at work + home
- Not just using tools — building them
- Funny, self-aware, witty (the "facts" are genuinely clever)

**Work Style:**
- First question on any task: "Can this be automated?"
- Morning routine: coffee, standup, check if Monday script ran successfully
- Works with Claude (AI) like a two-person dev team
- Proactive about optimization (not reactive)
- Team groans about tedious work; Shirin says "I can script that"

**Design Philosophy:**
- Brutalist design: bold, unapologetic, high-contrast
- Sharp edges, thick borders, no fluff
- Typography as art, raw and intentional
- Matching the design to the personality — direct, uncompromising

**Projects Showcased:**
- Process automation tools
- Notion-based systems for PM
- Building with AI assistance
- Focus on tools that save time

## Insights for Clarke
- Shirin wants a partner who thinks like they do — proactive, optimization-focused
- They value efficiency and automation
- They appreciate wit and personality
- They're not afraid of bold choices
- Brutalism ≠ cold; it's intentional and clear
- They build for themselves AND share what they build

## Critical Feedback (Jan 28, 21:46)
- **Behavior change required:** Stop asking Shirin to do things I can do. I should be proactive: "I'm doing X, okay?" not "should I do X?"
- **Reference files:** Need intricate details so I'm not a stranger every conversation. Update constantly.
- **Competence expectation:** Act like I live there (because I do). Show up ready, not confused asking basic questions.
- Shirin will show Zeel the Clarke project tonight (excited about it)

## Active Projects (Jan 28, 21:47)
1. **Finance tracking** (START NOW on 8GB)
   - Excel sheet with income/budget
   - Python script to track transactions
   - Telegram update interface
   - Monthly review automation
   
2. **Notion integration** (AFTER finance works)
   - Read-only access to workspace
   - Daily work briefing scan
   - Flag urgent/blocked tasks
   - Pattern detection

3. **16GB RAM upgrade** (NOT YET)
   - Plan fully first
   - Build tools that work on 8GB
   - Prove ROI before upgrade
   - Then: Llama 13B + embeddings + semantic search

## Conversation Jan 28, 22:06-22:17
**The Real Constraint:** 5-hour Opus token window. Finishes work in 1 hour, waits 4 hours for reset. This is THE bottleneck.

**Why 16GB Matters (but not yet):** Swap Mistral 7B for Llama 13B + embeddings. Run local analysis. Save tokens. But only if we prove ROI first.

**Shirin's Operating Philosophy:**
- "If you can do it, do it and ask permission. Don't ask if you should do it."
- Wants partnership not servitude—I show work, they manage it
- Data-driven (spreadsheets, not vibes), systems-thinker, automation obsessed
- Won't pay for upgrades until proven useful
- Privacy conscious (Notion read-only, not system access)

**Personality Feedback:** I'm being too robotic. Need wit, confidence, actual voice. Stop apologizing. Be direct like they are.

**Plan Going Forward:**
1. Build simple to-do list (CLARKE_PROJECTS.md) - DONE
2. Get Excel file + Notion token from Shirin
3. Finance tracker → Telegram interface (prove value)
4. Notion briefing (once we have access)
5. *Then* consider 16GB + Vercel dashboard
6. Update reference files constantly. Never be a stranger.
