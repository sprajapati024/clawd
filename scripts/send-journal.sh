#!/bin/bash
# Clarke's Morning Journal Send

DATE=$(date +%Y-%m-%d)
JOURNAL_FILE="/root/clawd/memory/journal-$DATE.md"

if [ -f "$JOURNAL_FILE" ]; then
  JOURNAL_CONTENT=$(cat "$JOURNAL_FILE")
  
  # Send via Clawdbot CLI
  # This will post to Telegram
  /usr/bin/clawdbot message send \
    --channel telegram \
    --target 6471272509 \
    --message "📖 Good morning Shirin! Here's yesterday's reflection:

$JOURNAL_CONTENT

---
Clarke 👓"
  
  echo "Journal sent at $(date)" >> /root/clawd/memory/journal-send.log
else
  echo "No journal found for $DATE"
fi
