#!/bin/bash
#
# Setup cron job for daily trading routine
# Runs Mon-Fri at 4:30 PM EST
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DAILY_ROUTINE="$SCRIPT_DIR/scripts/daily_routine.sh"

# Make scripts executable
chmod +x "$DAILY_ROUTINE"

# Add cron job (4:30 PM EST = 9:30 PM UTC in winter, 8:30 PM UTC in summer)
# Using 21:30 UTC for EST (winter), cron will handle DST
CRON_LINE="30 21 * * 1-5 cd /root/clawd/projects/day-trader && bash scripts/daily_routine.sh >> logs/cron.log 2>&1"

# Check if already exists
if crontab -l 2>/dev/null | grep -q "daily_routine.sh"; then
    echo "⚠️  Cron job already exists. Removing old one..."
    crontab -l 2>/dev/null | grep -v "daily_routine.sh" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -

echo "✅ Cron job installed successfully!"
echo ""
echo "📅 Schedule: Mon-Fri at 4:30 PM EST (9:30 PM UTC)"
echo "📂 Logs: /root/clawd/projects/day-trader/logs/"
echo "📊 Daily reports will be generated automatically"
echo ""
echo "Current crontab:"
crontab -l | grep "daily_routine.sh"
echo ""
echo "To view logs: tail -f /root/clawd/projects/day-trader/logs/cron.log"
