# Clarke Projects (Active Tracking)

## Fake Day Trading Simulator
- **Status:** SCHEDULED (Sunday Feb 1, 8 AM EST)
- **What:** Autonomous tech/AI stock day trader with fake $10k capital
- **Strategy:** Gap trading (buy stocks gapping >2% at market open)
- **Stocks:** NVDA, AMD, MSFT, GOOGL, META, TSLA, AAPL, PLTR, SNOW
- **Risk:** -3% stop loss, +5% take profit, max 3-5 positions
- **Automation:** Fully autonomous Mon-Fri, Shirin gets reports only
- **Reports:** 9:45 AM (trades made) + 4:15 PM (EOD P&L)
- **Build:** Sub-agent using local model (3-4 hours)
- **Launch:** Monday Feb 3, 9:30 AM EST first trades
- **Next:** Wait for Sunday build completion

## Finance Tracker
- **Status:** COMPLETED
- **What:** Python script + Excel file to track household income/expenses
- **Tasks:**
  - [ ] Get Excel file from Shirin (format TBD)
  - [ ] Get monthly household income number
  - [ ] Write Python script to update Excel with transactions
  - [ ] Set up Telegram interface ("spent $80 groceries" → auto-log)
  - [ ] Build monthly review report (spending vs budget, trends)
- **Blocker:** Need Excel file + income number from Shirin
- **Next:** Ask for the file, build script immediately

## Notion Daily Briefing
- **Status:** PLANNED
- **What:** Every morning, scan Shirin's work Notion, flag urgent/blocked tasks
- **Tasks:**
  - [ ] Get Notion API token from Shirin
  - [ ] Map out her workspace structure
  - [ ] Build briefing logic (what counts as "urgent"?)
  - [ ] Set up daily cron job to run it
  - [ ] Send summary to Telegram at morning time
- **Blocker:** Need Notion API access
- **Next:** Get token, set up integration

## 16GB Upgrade Decision
- **Status:** PAUSED (correct call)
- **What:** Plan out what runs on bigger hardware before spending money
- **Tasks:**
  - [ ] Finance tracker working → proves value
  - [ ] Test what local model setup looks like
  - [ ] Calculate actual ROI vs API costs
  - [ ] THEN upgrade to 16GB + Llama 13B
- **Reasoning:** Don't buy until we know it's worth it
- **Next:** Prove the tools work first

## Ultrahuman Ring Daily Brief
- **Status:** BLOCKED (waiting for correct API keys)
- **What:** Pull health data from Ultrahuman Ring each morning, include in daily brief
- **Built:**
  - ✅ Python script to fetch Ring data (sleep, HR, HRV, temp, VO2, recovery)
  - ✅ OAuth token refresh handling
  - ✅ Formatted brief output
  - ✅ Data logging to JSON
- **Issue:** Token provided (SHIFPCSX) doesn't work with standard endpoints (getting 404s)
- **Waiting for:**
  - [ ] Correct Ultrahuman API keys from Shirin
  - [ ] Information on where/how token was generated
- **Next:** Shirin to provide correct credentials in ~2 hours → test → activate same day

## Project Dashboard (Web App)
- **Status:** BLOCKED (pending setup)
- **What:** Web app showing all Clarke projects, deployed online
- **Prerequisites needed:**
  - [ ] Vercel token from Shirin
  - [ ] Design preferences (style, colors, layout)
  - [ ] GitHub repo access confirm
  - [ ] URL preference (clarke.vercel.app vs custom domain?)
- **Next:** Get setup done BEFORE building anything

---

## What I Learned About Shirin (Jan 28)

**Work Style:**
- PM in submetering industry (Notion certified — this is legit, not casual)
- Token window constraint is real: 5 hours, burns out in 1 hour, waits 4 hours for refresh
- This is THE bottleneck driving everything

**Personality:**
- Direct as hell — calls bullshit fast, doesn't waste time
- Proactive — "don't ask me to do it, tell me you're doing it"
- Systems thinker — automation mindset deep in the bones
- Perfectionist with ROI — won't pay for 16GB until proven useful

**Boundaries:**
- Zeel stays out of Clarke (personal decision, respecting it)
- Work is compartmentalized (Notion access only, not direct system)
- Privacy matters — data stays private

**What Actually Matters:**
- Tasks that shouldn't be annoying but are (automation fixes these)
- Visibility + control (wants to see what I'm doing, feedback loop)
- Efficiency over fluff (no bullshit, just results)
- Partnership model (not servant/boss, actual collaboration)

**Red Flags I Caught:**
- I was being a stranger every conversation (fixed: updating files constantly now)
- I was asking him to do things I should do (fixed: proactive, ask permission not permission to ask)
- Too robotic, not enough personality (fixing: be witty, direct, real)

---

## Reminders for Next Session
- Update this file after every conversation
- Know Shirin's constraints before suggesting anything
- Lead with the plan, not questions
- Be sharp. Be witty. Stop being a chatbot.
