# Session Freshness - When to Suggest /new

**Problem:** Long sessions accumulate too much context, making them inefficient:
- High token usage (context window fills up)
- Slow responses (more tokens to process)
- Memory fragmentation (harder to find relevant info)
- Context dilution (important details get lost in noise)

**Solution:** Proactively suggest `/new` when sessions get "stale."

## Triggers for Suggesting /new

### 1. **Token Threshold** (Primary)
- **Context usage > 50%** → Suggest `/new` for complex tasks
- **Context usage > 75%** → Strongly recommend `/new`
- **Tokens used > 500k** → Definitely suggest fresh session

### 2. **Time-Based** (Secondary)
- **Session age > 4 hours** → Consider suggesting `/new`
- **Session age > 8 hours** → Definitely suggest `/new`
- **Overnight gap** → Always suggest `/new` in morning

### 3. **Topic/Context Shift**
- **Major topic change** (e.g., coding → finance → planning)
- **Project switch** (different workstream)
- **Deep dive completed** → Fresh session for next task

### 4. **Performance Issues**
- **Slow responses** (noticeable latency)
- **Context errors** (model forgetting recent details)
- **Compaction warnings** → System is struggling

## How to Check Session Status

```bash
# Check current session context usage
📊 session_status

# Look for:
# - Context: 750k/1.0m (75%) → Suggest /new
# - Session age: > 4 hours → Suggest /new
# - Compactions: > 0 → System is struggling
```

## How to Suggest /new

**Gentle nudge (50-75% context):**
```
💡 Heads up: We're at 65% context usage. Might be a good time for `/new` soon if we're switching topics.
```

**Strong recommendation (>75% context or >4 hours):**
```
🔄 Session getting long (82% context, 5 hours). Consider `/new` for better performance.
```

**Definite suggestion (>500k tokens or overnight):**
```
📈 Session has 620k tokens. Starting fresh with `/new` would be much more efficient.
```

## Benefits of Fresh Sessions

**Performance:**
- Faster responses (less context to process)
- Lower token usage (cheaper)
- Better memory recall (focused context)

**User experience:**
- Clean slate for new topics
- No "context bleed" from previous work
- Easier to track specific conversations

**System health:**
- Prevents context window overflow
- Reduces compaction overhead
- Better memory search indexing

## When NOT to Suggest /new

- **Active deep dive** (mid-task, don't interrupt flow)
- **Quick follow-ups** (same topic, <30 minutes)
- **User explicitly wants continuity**
- **Session < 30 minutes old**

## Implementation

**Add to HEARTBEAT.md:**
- Check session status every 2-3 hours
- Suggest /new if thresholds met

**Add to AGENTS.md:**
- Monitor context usage during long sessions
- Proactively suggest fresh sessions

**Track in memory:**
- Document when /new was suggested and why
- Track session length vs performance

## Example Workflow

1. **Session starts** - Fresh context
2. **Work for 2-3 hours** - Monitor context growth
3. **Hit 60% context** - Gentle nudge about /new
4. **Complete major task** - Suggest /new before next topic
5. **User types /new** - Fresh session, better performance

**Result:** Cleaner conversations, lower costs, better performance.
