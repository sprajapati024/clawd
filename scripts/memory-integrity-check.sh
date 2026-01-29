#!/bin/bash
# Memory Integrity Checker - ensures memory files are up-to-date and not corrupted

WORKSPACE="/root/clawd"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d yesterday +%Y-%m-%d)
TODAY_FILE="$MEMORY_DIR/$TODAY.md"
YESTERDAY_FILE="$MEMORY_DIR/$YESTERDAY.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🧠 Memory Integrity Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

ISSUES=0

# Check if today's memory file exists
if [[ ! -f "$TODAY_FILE" ]]; then
    echo -e "${RED}❌ CRITICAL: Today's memory file missing!${NC}"
    echo "   Expected: $TODAY_FILE"
    ISSUES=$((ISSUES + 1))
else
    echo -e "${GREEN}✅ Today's memory file exists${NC}"
    
    # Check if file was modified recently (within last 6 hours during waking hours)
    CURRENT_HOUR=$(date +%H)
    if [[ $CURRENT_HOUR -ge 6 && $CURRENT_HOUR -le 23 ]]; then
        FILE_AGE=$(($(date +%s) - $(stat -c %Y "$TODAY_FILE")))
        MAX_AGE=$((6 * 3600))  # 6 hours in seconds
        
        if [[ $FILE_AGE -gt $MAX_AGE ]]; then
            echo -e "${YELLOW}⚠️  WARNING: Today's memory file hasn't been updated in $(($FILE_AGE / 3600)) hours${NC}"
            ISSUES=$((ISSUES + 1))
        else
            echo -e "${GREEN}✅ Today's memory file is recent${NC}"
        fi
    fi
fi

# Check if yesterday's memory file exists
if [[ ! -f "$YESTERDAY_FILE" ]]; then
    echo -e "${YELLOW}⚠️  Yesterday's memory file missing${NC}"
    echo "   Expected: $YESTERDAY_FILE"
else
    echo -e "${GREEN}✅ Yesterday's memory file exists${NC}"
fi

# Check for corrupted files (basic validation)
for file in "$TODAY_FILE" "$YESTERDAY_FILE"; do
    if [[ -f "$file" ]]; then
        # Check if file is readable and has content
        if [[ ! -r "$file" ]]; then
            echo -e "${RED}❌ CRITICAL: Cannot read $file${NC}"
            ISSUES=$((ISSUES + 1))
        elif [[ ! -s "$file" ]]; then
            echo -e "${RED}❌ CRITICAL: $file is empty!${NC}"
            ISSUES=$((ISSUES + 1))
        fi
    fi
done

# Check git status
cd "$WORKSPACE" || exit 1
if ! git diff --quiet memory/; then
    echo -e "${YELLOW}⚠️  Uncommitted memory changes detected${NC}"
    echo "   Running auto-commit..."
    bash "$WORKSPACE/scripts/memory-auto-commit.sh"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [[ $ISSUES -eq 0 ]]; then
    echo -e "${GREEN}✅ Memory integrity: PASS${NC}"
    exit 0
else
    echo -e "${RED}❌ Memory integrity: FAIL ($ISSUES issues)${NC}"
    exit 1
fi
