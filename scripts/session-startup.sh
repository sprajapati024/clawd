#!/bin/bash
# Session startup hook - runs on every new chat session
# Loads recent memory context automatically

WORKSPACE="/root/clawd"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

echo "🔍 Session startup: Loading memory context..."

# Ensure memory directory exists
mkdir -p "$MEMORY_DIR"

# Create today's memory file if it doesn't exist
if [ ! -f "$MEMORY_DIR/$TODAY.md" ]; then
    echo "# Memory - $TODAY" > "$MEMORY_DIR/$TODAY.md"
    echo "" >> "$MEMORY_DIR/$TODAY.md"
    echo "📝 Created today's memory file: $TODAY.md"
else
    echo "📝 Today's memory: $TODAY.md exists"
fi

# Check yesterday's file
if [ -f "$MEMORY_DIR/$YESTERDAY.md" ]; then
    echo "📝 Yesterday's memory: $YESTERDAY.md exists"
fi

# Memory stats (if CLI exists)
if [ -f "$WORKSPACE/scripts/memory" ]; then
    bash "$WORKSPACE/scripts/memory" stats 2>/dev/null || true
fi

# Remind about key files to read
echo ""
echo "📖 Remember to read:"
echo "   - SOUL.md (who you are)"
echo "   - USER.md (who Shirin is)"
echo "   - MEMORY.md (long-term memory, main session only)"
echo "   - memory/$TODAY.md + memory/$YESTERDAY.md (recent context)"
echo ""
echo "🔍 Use 'memory search <query>' before re-reading files"
echo "✅ Session startup complete"
