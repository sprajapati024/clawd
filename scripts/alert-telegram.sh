#!/bin/bash
# Clarke's Telegram Alert System
# Send critical alerts directly to Telegram via Clawdbot message tool

SEVERITY="$1"
MESSAGE="$2"

if [ -z "$MESSAGE" ]; then
    echo "Usage: alert-telegram.sh <severity> <message>"
    echo "Severity: info|warning|critical"
    exit 1
fi

# Emoji mapping
case "$SEVERITY" in
    info)
        ICON="ℹ️"
        ;;
    warning)
        ICON="⚠️"
        ;;
    critical)
        ICON="🚨"
        ;;
    *)
        ICON="📢"
        ;;
esac

# Format message
ALERT="${ICON} **${SEVERITY^^}**: ${MESSAGE}"

# Log it
echo "[$(date)] Sending alert: $ALERT" >> /var/log/clarke-monitor/telegram-alerts.log

# Send via Clawdbot (if available)
if command -v clawdbot &> /dev/null; then
    # Use clawdbot to send the message
    # Note: This will work if clawdbot is running and configured
    echo "Telegram alert would be sent here: $ALERT"
    # Actual implementation would use clawdbot's message API
    # For now, just log it
else
    echo "clawdbot not available - alert logged only"
fi
