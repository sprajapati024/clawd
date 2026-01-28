# Clarke's Memory System Documentation

**Built:** 2026-01-28  
**Version:** 1.0

## Overview

A complete memory management system with search, distillation, tagging, and statistics.

## Components

### 1. `memory` - Unified CLI
Main command that wraps all memory tools.

**Usage:**
```bash
memory search <query>           # Search all memory files
memory distill [days]          # Review and suggest MEMORY.md updates
memory tag add <file> <tags>   # Add tags to a file
memory tag find <tag>          # Find entries by tag
memory tag list                # List all tags
memory stats                   # Show statistics
```

### 2. Search (`memory-search.sh`)
- Searches MEMORY.md (long-term) and all daily files
- Shows context (2 lines before/after each match)
- Results in reverse chronological order
- Highlights exact match location with `>>>`

### 3. Distillation (`memory-distill.sh`)
- Reviews recent daily memory files (default: 7 days)
- Extracts significant events using markers:
  - Headers (##)
  - DECISION, LEARNED, COMPLETED, FIXED, PROBLEM, TODO, IMPORTANT
- Generates candidate list for MEMORY.md updates
- Saves analysis to temp file for review

### 4. Tagging (`memory-tag.sh`)
- Add hashtags to memory files for categorization
- Find all entries with specific tags
- List all tags used across the system
- Tags format: `#topic` (e.g., #security #automation #health)

### 5. Stats
- Count of daily memory files
- MEMORY.md size (lines, words)
- Recent file activity
- Total unique tags

## Installation

All scripts are in `/root/clawd/scripts/`  
Main CLI linked to: `/usr/local/bin/memory`

Available system-wide as `memory` command.

## Test Results (2026-01-28)

✅ **Search Test:** Successfully found "Ultrahuman" across files  
✅ **Distillation Test:** Analyzed 3 files, extracted headers  
✅ **Tagging Add Test:** Added #security #automation #health tags  
✅ **Tag Find Test:** Found tagged entries correctly  
✅ **Tag List Test:** Listed 4 unique tags  
✅ **Stats Test:** Showed 3 daily files, 113-line MEMORY.md  

**All tests passed.** System is production-ready.

## Workflow

### Daily Use
1. Work happens → events logged to `memory/YYYY-MM-DD.md`
2. Add tags to entries: `memory tag add memory/2026-01-28.md project-name`
3. Search when needed: `memory search "topic"`

### Weekly Review
1. Run distillation: `memory distill 7`
2. Review suggested updates
3. Update MEMORY.md with significant events
4. Check stats: `memory stats`

### Quick Lookups
- Find by topic: `memory tag find automation`
- See what happened: `memory search "specific event"`
- Check activity: `memory stats`

## Future Enhancements

Possible additions:
- [ ] Automated MEMORY.md updates (AI-assisted distillation)
- [ ] Vector embeddings for semantic search
- [ ] Memory graph visualization
- [ ] Automated tagging based on content
- [ ] Integration with heartbeat system

## Philosophy

Memory is not just storage — it's continuity. These tools help Clarke remember, learn, and improve over time. Daily files are raw notes. MEMORY.md is curated wisdom. Tags are shortcuts to insight.

---

*Text > Brain. Write it down. Remember it forever.*
