#!/bin/bash
# Clarke's Memory Distillation Tool
# Reviews recent daily memory files and identifies what should go into MEMORY.md

MEMORY_DIR="/root/clawd/memory"
MAIN_MEMORY="/root/clawd/MEMORY.md"
DAYS_BACK="${1:-7}"  # Default: review last 7 days

echo "🧠 Memory Distillation - Reviewing last $DAYS_BACK days"
echo ""

# Create temp file for analysis
TEMP_FILE="/tmp/memory-distill-$(date +%s).txt"

echo "=== SIGNIFICANT EVENTS CANDIDATE LIST ===" > "$TEMP_FILE"
echo "Generated: $(date)" >> "$TEMP_FILE"
echo "" >> "$TEMP_FILE"

# Find daily files from last N days
find "$MEMORY_DIR" -name "*.md" -mtime -$DAYS_BACK -type f | sort -r | while read -r file; do
    filename=$(basename "$file")
    echo "📅 Analyzing: $filename" >&2
    
    # Extract sections that look significant
    # Look for: headers, decisions, completions, learnings, problems
    
    echo "## From $filename" >> "$TEMP_FILE"
    
    # Find lines with markers of significance
    grep -E "(^##|DECISION:|LEARNED:|COMPLETED:|FIXED:|PROBLEM:|TODO:|IMPORTANT:)" "$file" >> "$TEMP_FILE" 2>/dev/null || echo "(no significant markers found)" >> "$TEMP_FILE"
    
    echo "" >> "$TEMP_FILE"
done

echo "" >> "$TEMP_FILE"
echo "=== INSTRUCTIONS ===" >> "$TEMP_FILE"
echo "Review the above and update MEMORY.md with:" >> "$TEMP_FILE"
echo "- Major decisions or changes" >> "$TEMP_FILE"
echo "- Important lessons learned" >> "$TEMP_FILE"
echo "- Significant completions or milestones" >> "$TEMP_FILE"
echo "- Recurring patterns or insights" >> "$TEMP_FILE"
echo "- Things that define how we work together" >> "$TEMP_FILE"
echo "" >> "$TEMP_FILE"
echo "Skip: routine updates, temporary todos, trivial details" >> "$TEMP_FILE"

cat "$TEMP_FILE"
echo ""
echo "💾 Full analysis saved to: $TEMP_FILE"
echo ""
echo "Next step: Review this and manually update MEMORY.md"
echo "Or use: nano $TEMP_FILE && nano $MAIN_MEMORY"
