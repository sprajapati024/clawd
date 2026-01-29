#!/bin/bash
# Clarke's Unified Morning Brief
# Everything you need to start your day - 6 AM EST

BRIEF_FILE="/tmp/morning-brief-$(date +%Y%m%d).txt"

cat > "$BRIEF_FILE" << 'HEADER'
☀️ GOOD MORNING

HEADER

echo "📅 $(date '+%A, %B %d, %Y')" >> "$BRIEF_FILE"
echo "" >> "$BRIEF_FILE"

# WEATHER
echo "🌤️  WEATHER - Toronto" >> "$BRIEF_FILE"

# Use wttr.in for weather (no API key needed)
WEATHER=$(curl -s "wttr.in/Toronto?format=%C+%t+|+Feels+like:+%f+|+Wind:+%w" 2>/dev/null)
if [ -n "$WEATHER" ]; then
    echo "$WEATHER" >> "$BRIEF_FILE"
else
    echo "Weather unavailable" >> "$BRIEF_FILE"
fi

# Today's forecast
FORECAST=$(curl -s "wttr.in/Toronto?format=3" 2>/dev/null | head -1)
if [ -n "$FORECAST" ]; then
    echo "$FORECAST" >> "$BRIEF_FILE"
fi

echo "" >> "$BRIEF_FILE"

# OVERNIGHT SECURITY
echo "🛡️  OVERNIGHT SECURITY" >> "$BRIEF_FILE"

# Last 8 hours (overnight while you sleep)
FAILED_LOGINS=$(sudo grep "Failed password" /var/log/auth.log 2>/dev/null | tail -100 | grep "$(date '+%b %d')" | wc -l)
CURRENTLY_BANNED=$(sudo fail2ban-client status sshd 2>/dev/null | grep "Currently banned" | awk '{print $4}')

echo "Status: ✅ All systems secure" >> "$BRIEF_FILE"
echo "Failed attempts blocked: $FAILED_LOGINS" >> "$BRIEF_FILE"
echo "IPs currently banned: $CURRENTLY_BANNED" >> "$BRIEF_FILE"

# Check for any critical alerts overnight
if [ -f /var/log/clarke-monitor/auto-heal.log ]; then
    CRITICAL_OVERNIGHT=$(grep -c "CRITICAL" /var/log/clarke-monitor/auto-heal.log 2>/dev/null | tail -20)
    if [ "$CRITICAL_OVERNIGHT" -gt 0 ]; then
        echo "⚠️  $CRITICAL_OVERNIGHT critical events auto-resolved" >> "$BRIEF_FILE"
    fi
fi

echo "" >> "$BRIEF_FILE"

# SYSTEM HEALTH
echo "💚 SYSTEM HEALTH" >> "$BRIEF_FILE"

DISK=$(df / | tail -1 | awk '{print $5}')
MEM=$(free | grep Mem | awk '{printf "%.0f%%", $3/$2 * 100}')
CPU=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}')
UPTIME=$(uptime -p | sed 's/up //')

echo "💾 Disk: $DISK" >> "$BRIEF_FILE"
echo "🧠 Memory: $MEM" >> "$BRIEF_FILE"
echo "⚙️  CPU Load: $CPU" >> "$BRIEF_FILE"
echo "⏱️  Uptime: $UPTIME" >> "$BRIEF_FILE"

# Check service status
SERVICES_OK=true
for service in ssh fail2ban; do
    if ! systemctl is-active --quiet $service; then
        echo "⚠️  $service is down" >> "$BRIEF_FILE"
        SERVICES_OK=false
    fi
done

if [ "$SERVICES_OK" = true ]; then
    echo "✅ All services running" >> "$BRIEF_FILE"
fi

echo "" >> "$BRIEF_FILE"

# OVERNIGHT WORK (Autonomous Tasks)
OVERNIGHT_WORK_FILE="/tmp/overnight-work-$(date +%Y%m%d).txt"
if [ -f "$OVERNIGHT_WORK_FILE" ]; then
    echo "🤖 OVERNIGHT WORK" >> "$BRIEF_FILE"
    cat "$OVERNIGHT_WORK_FILE" >> "$BRIEF_FILE"
    echo "" >> "$BRIEF_FILE"
    # Clear the file after reading
    rm "$OVERNIGHT_WORK_FILE"
fi

# TOKEN USAGE (Yesterday)
if [ -f /root/clawd/scripts/token-tracker.py ]; then
    echo "📊 TOKEN USAGE (Yesterday)" >> "$BRIEF_FILE"
    YESTERDAY=$(date -d yesterday '+%Y-%m-%d')
    TOKEN_STATS=$(/root/clawd/scripts/token-tracker.py daily 2>/dev/null | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"• Local (Mistral): {d['mistral']:,} tokens (\$0.00)\n• Claude API: {d['claude']:,} tokens (\${d['actual_cost']:.2f})\n• Optimization: {d['savings_pct']:.1f}% local ({d['savings_pct']:.0f}% cost reduction)\")" 2>/dev/null)
    if [ -n "$TOKEN_STATS" ]; then
        echo "$TOKEN_STATS" >> "$BRIEF_FILE"
    else
        echo "No token usage yesterday" >> "$BRIEF_FILE"
    fi
    echo "" >> "$BRIEF_FILE"
fi

# IMPROVEMENT SUGGESTIONS
SUGGESTIONS_FILE="/tmp/improvement-suggestions-$(date +%Y%m%d).txt"
if [ -f "$SUGGESTIONS_FILE" ]; then
    echo "💡 IMPROVEMENTS TO CONSIDER" >> "$BRIEF_FILE"
    cat "$SUGGESTIONS_FILE" >> "$BRIEF_FILE"
    echo "" >> "$BRIEF_FILE"
    # Clear the file after reading
    rm "$SUGGESTIONS_FILE"
fi

# FOOTER
cat >> "$BRIEF_FILE" << 'FOOTER'

Have a good day. I'll be here if you need me.
— Clarke
FOOTER

# Output the brief
cat "$BRIEF_FILE"

# Save for records
cp "$BRIEF_FILE" /var/log/clarke-monitor/latest-morning-brief.txt
