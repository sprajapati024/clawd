#!/bin/bash
# Memory writing enforcement - reminds if memory hasn't been written recently

MEMORY_DIR="/root/clawd/memory"
TODAY=$(date +%Y-%m-%d)
MEMORY_FILE="$MEMORY_DIR/$TODAY.md"

# Check if today's memory file exists
if [ ! -f "$MEMORY_FILE" ]; then
    echo "⚠️  WARNING: Today's memory file doesn't exist yet!"
    echo "   Create: $MEMORY_FILE"
    exit 1
fi

# Check last modification time
LAST_MOD=$(stat -c %Y "$MEMORY_FILE")
NOW=$(date +%s)
SECONDS_AGO=$((NOW - LAST_MOD))
MINUTES_AGO=$((SECONDS_AGO / 60))

if [ $MINUTES_AGO -gt 30 ]; then
    echo "⚠️  WARNING: Memory file last modified $MINUTES_AGO minutes ago"
    echo "   Have you written down recent work?"
    echo "   File: $MEMORY_FILE"
    exit 1
fi

# Check if there are uncommitted memory changes
cd /root/clawd
if git status --porcelain | grep -q "memory/"; then
    echo "⚠️  WARNING: Uncommitted memory changes detected"
    echo "   Run: bash /root/clawd/scripts/memory-auto-commit.sh"
    exit 1
fi

echo "✅ Memory up to date (last write $MINUTES_AGO min ago, committed)"
exit 0
