# Multi-Agent System

Three specialist agents for focused, expert work.

## Agents

### 1. **Ledger** (Finance Agent)
**Role:** Track spending, budget summaries, financial reporting
**Files:** `/root/clawd/agents/ledger/`
**Model:** DeepSeek (cost-efficient)
**Invoke:** `@ledger` or via router

### 2. **Atlas** (PM Agent)  
**Role:** Todoist management, task tracking, project status
**Files:** `/root/clawd/agents/atlas/`
**Model:** Sonnet (strategic thinking)
**Todoist Integration:** Full CLI access, auto-sync on heartbeat
**Invoke:** `@atlas` or via router

**Atlas Rules:**
- ✅ Mark tasks done
- ✅ Add progress comments
- ❌ NEVER delete tasks
- 📊 Regular status reports

### 3. **Forge** (Developer Agent)
**Role:** Code, scripts, automation, debugging
**Files:** `/root/clawd/agents/forge/`
**Model:** Sonnet for complex, DeepSeek for boilerplate
**Invoke:** `@forge` or via router

## Usage

### Direct invocation (via Clarke):
```
"@ledger show me September spending"
"@atlas what's on my plate today?"
"@forge write a Python script to parse CSV"
```

### Via router script:
```bash
/root/clawd/agents/router.sh ledger "add $50 groceries"
/root/clawd/agents/router.sh atlas "mark task #123 done"
/root/clawd/agents/router.sh forge "debug this bash script"
```

### Automatic routing:
Clarke (main agent) automatically routes based on context:
- Finance questions → Ledger
- Task/project management → Atlas  
- Code/technical work → Forge

## Organization

**You (Shirin)** → **Clarke (CEO)** → **Specialists (Atlas, Forge, Ledger)**

### Clarke as CEO:
- Manages the specialist team
- Delegates tasks based on expertise
- Reviews and synthesizes specialist outputs
- Reports results to you
- Makes routine decisions, escalates major ones

### Specialists report to Clarke:
- Execute assigned work in their domain
- Report results back to Clarke
- Escalate blockers and decisions to Clarke
- Never act externally without approval

**See `/root/clawd/ORGANIZATION.md` for full hierarchy.**

## File Structure

```
/root/clawd/agents/
├── README.md           # This file
├── router.sh           # Routing script
├── ledger/
│   ├── ROLE.md        # Agent purpose
│   ├── KNOWLEDGE.md   # Domain expertise
│   ├── EXAMPLES.md    # Usage examples
│   └── config.json    # Settings
├── atlas/
│   ├── ROLE.md
│   ├── KNOWLEDGE.md   # Todoist CLI commands
│   ├── EXAMPLES.md
│   └── config.json    # Todoist settings
└── forge/
    ├── ROLE.md
    ├── KNOWLEDGE.md
    ├── EXAMPLES.md
    └── config.json
```

## Testing

Test each agent:
```bash
# Ledger test (placeholder - no live data yet)
echo "Test: Ledger ready"

# Atlas test (requires Todoist CLI configured)
todoist today

# Forge test  
echo "Test: Forge ready for code tasks"
```

## Next Steps

1. **Ledger:** Set up transaction data directory (`/root/clawd/data/ledger/`)
2. **Atlas:** Verify Todoist CLI is authenticated (`todoist sync`)
3. **Forge:** Test code generation with simple script request
4. **Integration:** Train Clarke on routing patterns

## Notes

- Each agent loads its playbook on invocation
- Playbooks are editable—update as workflows evolve
- Atlas never deletes tasks (archive-only workflow)
- All agents respect privacy boundaries
