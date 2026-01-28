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
