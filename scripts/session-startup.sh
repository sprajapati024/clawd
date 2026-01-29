#!/bin/bash
# Session startup hook - runs on every new chat session
# Loads recent memory context automatically

WORKSPACE="/root/clawd"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

echo "🔍 Session startup: Loading memory context..."

# Check if memory CLI exists
if [ -f "$WORKSPACE/scripts/memory" ]; then
    # Search for today's context
    if [ -f "$MEMORY_DIR/$TODAY.md" ]; then
        echo "📝 Today's memory: $TODAY.md exists"
    fi
    
    # Check yesterday's file
    if [ -f "$MEMORY_DIR/$YESTERDAY.md" ]; then
        echo "📝 Yesterday's memory: $YESTERDAY.md exists"
    fi
    
    # Quick stats
    bash "$WORKSPACE/scripts/memory" stats 2>/dev/null || true
else
    echo "⚠️  Memory CLI not found at $WORKSPACE/scripts/memory"
fi

echo "✅ Session startup complete"
