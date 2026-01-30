# Memory Search Discipline - Examples

## ❌ Bad: Jump straight to answer or file read

**User:** "What cron jobs did we remove today?"

**Bad response:**
```
Let me check... [reads CRON.json, reads memory file]
We removed gmail-scan, daily-security-report, and system-cleanup-logging.
```

**Problem:** Wasted tokens re-reading files that were already indexed.

---

## ✅ Good: Search first, then targeted read

**User:** "What cron jobs did we remove today?"

**Good response:**
```
[runs memory_search "cron jobs removed optimization"]
Found it - we removed 3 cron jobs today:
- gmail-scan (per your request)
- daily-security-report (moved to heartbeat)
- system-cleanup-logging (moved to heartbeat)

Part of Option C implementation for cron optimization.
```

**Why better:** Direct hit from search, no file re-reading needed.

---

## When Search Returns Nothing

**User:** "What did we discuss about DeepSeek yesterday?"

**Honest response:**
```
[runs memory_search "deepseek api configuration"]
I searched memory but found nothing yet - indexing might be catching up.
Let me check yesterday's memory file directly...
[reads memory/2026-01-29.md, finds DeepSeek section]

Found it - we researched DeepSeek API setup for model fallback...
```

**Why honest:** Admitted search came up empty, explained why, then fell back to direct read.

---

## Mandatory Search Triggers (Checklist)

Before responding to these types of questions, **ALWAYS search first:**

- [ ] "What did we build...?"
- [ ] "When did we...?"
- [ ] "Why did we decide...?"
- [ ] "What's on my todo list?"
- [ ] "What does [person] prefer?"
- [ ] "Have we tried this before?"
- [ ] "What was the outcome of...?"
- [ ] "Remind me about..."

---

## Search → Get → Answer Pattern

```bash
# 1. Search broadly
memory_search "topic keywords"

# 2. If results found, get specific lines
memory_get --path memory/2026-01-29.md --from 150 --lines 20

# 3. Answer with specific reference
"Found it in yesterday's memory (lines 150-170)..."
```

---

## Token Efficiency Comparison

**Without search:**
- Read MEMORY.md: ~2000 tokens
- Read today's memory: ~500 tokens
- Read yesterday's memory: ~800 tokens
- **Total: ~3300 tokens**

**With search:**
- Search query: ~50 tokens
- Get specific section: ~200 tokens
- **Total: ~250 tokens**

**Savings: ~92% fewer tokens** for targeted recall.

---

## Anti-Patterns to Avoid

❌ **"I remember..."** - You don't remember. Search or admit you're guessing.
❌ **Re-reading same file multiple times** - Search should prevent this.
❌ **Vague answers** - Search gives you line numbers for specifics.
❌ **Pretending to search** - Be honest if you skip it.

---

## When NOT to Search

- Brand new information in current session
- Questions about general knowledge (not personal memory)
- File you're about to edit (need full context anyway)
- Bootstrap files (SOUL.md, USER.md, AGENTS.md) - read these fresh
