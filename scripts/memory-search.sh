#!/bin/bash
# Clarke's Memory Search Tool
# Smart search across all memory files with context and ranking

QUERY="$1"
MEMORY_DIR="/root/clawd/memory"
MAIN_MEMORY="/root/clawd/MEMORY.md"

if [ -z "$QUERY" ]; then
    echo "Usage: memory-search.sh <search query>"
    exit 1
fi

echo "🔍 Searching memory for: '$QUERY'"
echo ""

# Search MEMORY.md first (highest priority)
if [ -f "$MAIN_MEMORY" ]; then
    echo "=== LONG-TERM MEMORY (MEMORY.md) ==="
    grep -in --color=never "$QUERY" "$MAIN_MEMORY" | while IFS=: read -r line_num match; do
        # Get context (2 lines before and after)
        start=$((line_num - 2))
        [ $start -lt 1 ] && start=1
        end=$((line_num + 2))
        
        echo "📌 Line $line_num:"
        sed -n "${start},${end}p" "$MAIN_MEMORY" | sed "${line_num}s/^/>>> /"
        echo ""
    done
fi

# Search daily memory files (reverse chronological - newest first)
if [ -d "$MEMORY_DIR" ]; then
    echo "=== DAILY MEMORY FILES ==="
    for file in $(ls -t "$MEMORY_DIR"/*.md 2>/dev/null); do
        matches=$(grep -in "$QUERY" "$file" 2>/dev/null)
        if [ -n "$matches" ]; then
            filename=$(basename "$file")
            echo "📅 $filename"
            echo "$matches" | while IFS=: read -r line_num match; do
                start=$((line_num - 1))
                [ $start -lt 1 ] && start=1
                end=$((line_num + 1))
                
                sed -n "${start},${end}p" "$file" | sed "${line_num}s/^/>>> /"
                echo ""
            done
        fi
    done
fi

echo "✅ Search complete"
