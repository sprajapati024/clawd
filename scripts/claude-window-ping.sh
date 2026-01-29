#!/bin/bash
# Claude Pro Window Ping - Keeps 5-hour window cycling on schedule
# Makes minimal API call to start/renew the token window

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S %Z')
LOG_FILE="/root/clawd/logs/claude-ping.log"

mkdir -p /root/clawd/logs

echo "[$TIMESTAMP] Claude window ping initiated" >> "$LOG_FILE"

# Use Clawdbot's message tool to send a minimal ping to yourself
# This triggers Claude API usage and starts/renews the window
clawdbot message send \
  --channel telegram \
  --target 6471272509 \
  --message "🔄 Claude window refresh: $TIMESTAMP" \
  >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "[$TIMESTAMP] ✅ Window ping successful" >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] ❌ Window ping failed" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
