#!/bin/bash
# Send Daily Security Report to Telegram via Clawdbot

# Generate the report
REPORT=$(/root/clawd/scripts/security-daily-report.sh 2>/dev/null)

# Save to file for records
echo "$REPORT" > /var/log/clarke-monitor/latest-security-report.txt

# Send via Clawdbot message tool
# The report is formatted for Telegram markdown
echo "$REPORT" | head -100  # Limit to avoid message length issues

# Log that it was sent
echo "[$(date)] Security report generated and ready" >> /var/log/clarke-monitor/report-sends.log
