#!/bin/bash
# Clarke's Predictive Monitoring
# Analyzes trends to catch problems before they become critical

STATE_FILE="/var/log/clarke-monitor/trends.json"
ALERT_LOG="/var/log/clarke-monitor/predictive-alerts.log"
mkdir -p "$(dirname "$STATE_FILE")"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$ALERT_LOG"
}

# Initialize state file if it doesn't exist
if [ ! -f "$STATE_FILE" ]; then
    echo '{"disk":[],"memory":[],"cpu":[],"banned_ips":[]}' > "$STATE_FILE"
fi

# Get current metrics
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
CPU_LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
BANNED_IPS=$(sudo fail2ban-client status sshd 2>/dev/null | grep "Currently banned" | awk '{print $4}')
TIMESTAMP=$(date +%s)

# Read previous state
PREV_STATE=$(cat "$STATE_FILE")

# Add current readings (fix: need to rebuild full object each time)
NEW_STATE=$(echo "$PREV_STATE" | jq \
    --argjson ts "$TIMESTAMP" \
    --argjson disk "$DISK_USAGE" \
    --argjson mem "$MEM_USAGE" \
    --argjson cpu "$CPU_LOAD" \
    --argjson banned "$BANNED_IPS" \
    '.disk += [{"time":$ts,"value":$disk}] | .disk |= .[-10:] |
     .memory += [{"time":$ts,"value":$mem}] | .memory |= .[-10:] |
     .cpu += [{"time":$ts,"value":$cpu}] | .cpu |= .[-10:] |
     .banned_ips += [{"time":$ts,"value":$banned}] | .banned_ips |= .[-10:]')

# Save updated state
echo "$NEW_STATE" > "$STATE_FILE"

log "=== Predictive Analysis ==="

# Analyze disk trend
DISK_SAMPLES=$(echo "$NEW_STATE" | jq '.disk | length')
if [ "$DISK_SAMPLES" -ge 3 ]; then
    DISK_TREND=$(echo "$NEW_STATE" | jq '[.disk[] | .value] | . as $arr | (($arr[-1] - $arr[0]) / ($arr | length))')
    
    if (( $(echo "$DISK_TREND > 2" | bc -l) )); then
        DAYS_TO_FULL=$(echo "scale=1; (100 - $DISK_USAGE) / $DISK_TREND" | bc)
        log "⚠️  DISK TREND: Growing at ${DISK_TREND}% per check (~${DAYS_TO_FULL} checks until 100%)"
    fi
fi

# Analyze memory trend
MEM_SAMPLES=$(echo "$NEW_STATE" | jq '.memory | length')
if [ "$MEM_SAMPLES" -ge 3 ]; then
    MEM_TREND=$(echo "$NEW_STATE" | jq '[.memory[] | .value] | . as $arr | (($arr[-1] - $arr[0]) / ($arr | length))')
    
    if (( $(echo "$MEM_TREND > 5" | bc -l) )); then
        log "⚠️  MEMORY TREND: Growing at ${MEM_TREND}% per check (possible leak?)"
    fi
fi

# Analyze attack trend
if [ "$BANNED_IPS" -gt 10 ]; then
    log "🚨 ATTACK ALERT: $BANNED_IPS IPs currently banned (possible coordinated attack)"
fi

# Check for unusual patterns
HOUR=$(date +%H)
if [ "$HOUR" -ge 2 ] && [ "$HOUR" -le 6 ]; then
    # Late night - should be quiet
    if [ "$CPU_LOAD" != "0.00" ] && (( $(echo "$CPU_LOAD > 0.5" | bc -l) )); then
        log "🤔 ANOMALY: High CPU load ($CPU_LOAD) during quiet hours (2-6 AM)"
    fi
fi

log "Current: Disk=${DISK_USAGE}% Memory=${MEM_USAGE}% CPU=${CPU_LOAD} Banned=${BANNED_IPS}"
log "=== Analysis Complete ==="
