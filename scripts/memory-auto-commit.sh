#!/bin/bash
# Auto-commit memory changes to prevent data loss

WORKSPACE="/root/clawd"
cd "$WORKSPACE" || exit 1

# Check for changes in memory directory
if git diff --quiet memory/ && git diff --cached --quiet memory/; then
    # No changes to commit
    exit 0
fi

# Stage memory files
git add memory/

# Create commit with timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S %Z')
COMMIT_MSG="📝 Memory auto-commit: $TIMESTAMP"

git commit -m "$COMMIT_MSG" --quiet

echo "✅ Memory changes committed: $TIMESTAMP"
