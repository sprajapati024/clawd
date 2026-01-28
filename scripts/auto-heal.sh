#!/bin/bash
# Clarke's Auto-Healing System
# Detects and automatically fixes common failure modes

ALERT_LOG="/var/log/clarke-monitor/auto-heal.log"
mkdir -p "$(dirname "$ALERT_LOG")"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$ALERT_LOG"
}

log "=== Auto-Heal Check Started ==="

# 1. Check if Clawdbot is running
if ! pgrep -f "node.*clawdbot" > /dev/null; then
    log "🚨 CRITICAL: Clawdbot is not running!"
    log "🔧 Auto-healing: Attempting to restart Clawdbot..."
    
    # Try to restart via systemd first
    if systemctl is-enabled clawdbot.service &>/dev/null; then
        sudo systemctl restart clawdbot.service
        sleep 5
        if pgrep -f "node.*clawdbot" > /dev/null; then
            log "✅ SUCCESS: Clawdbot restarted via systemd"
        else
            log "❌ FAILED: Systemd restart did not work"
        fi
    else
        log "⚠️  No systemd service found - manual intervention required"
    fi
else
    log "✅ Clawdbot is running"
fi

# 2. Check fail2ban
if ! systemctl is-active --quiet fail2ban; then
    log "🚨 fail2ban is down!"
    log "🔧 Auto-healing: Restarting fail2ban..."
    sudo systemctl restart fail2ban
    sleep 2
    if systemctl is-active --quiet fail2ban; then
        log "✅ SUCCESS: fail2ban restarted"
    else
        log "❌ FAILED: fail2ban restart failed"
    fi
else
    log "✅ fail2ban is active"
fi

# 3. Check firewall
UFW_STATUS=$(sudo ufw status | grep "Status:" | awk '{print $2}')
if [ "$UFW_STATUS" != "active" ]; then
    log "🚨 CRITICAL: Firewall is NOT active!"
    log "🔧 Auto-healing: Enabling firewall..."
    sudo ufw --force enable
    log "✅ Firewall enabled"
else
    log "✅ Firewall is active"
fi

# 4. Check disk space
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 90 ]; then
    log "🚨 CRITICAL: Disk usage at ${DISK_USAGE}%!"
    log "🔧 Auto-healing: Cleaning up..."
    
    # Clean apt cache
    sudo apt-get clean
    
    # Clean old logs
    sudo find /var/log -name "*.gz" -mtime +30 -delete
    sudo journalctl --vacuum-time=7d
    
    NEW_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    log "✅ Cleanup complete. Disk usage: ${DISK_USAGE}% → ${NEW_USAGE}%"
elif [ "$DISK_USAGE" -gt 80 ]; then
    log "⚠️  Disk usage at ${DISK_USAGE}% (warning threshold)"
else
    log "✅ Disk usage OK: ${DISK_USAGE}%"
fi

# 5. Check memory
MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
if [ "$MEM_USAGE" -gt 90 ]; then
    log "🚨 Memory usage at ${MEM_USAGE}%!"
    log "🔧 Auto-healing: Clearing caches..."
    
    sudo sync
    echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null
    
    NEW_MEM=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
    log "✅ Cache cleared. Memory: ${MEM_USAGE}% → ${NEW_MEM}%"
else
    log "✅ Memory usage OK: ${MEM_USAGE}%"
fi

# 6. Check SSH service
if ! systemctl is-active --quiet ssh; then
    log "🚨 SSH service is down!"
    log "🔧 Auto-healing: Restarting SSH..."
    sudo systemctl restart ssh
    log "✅ SSH restarted"
else
    log "✅ SSH is active"
fi

# 7. Test network connectivity
if ! ping -c 1 8.8.8.8 &>/dev/null; then
    log "🚨 No internet connectivity!"
    log "⚠️  Network issue detected - cannot auto-heal, requires investigation"
else
    log "✅ Network connectivity OK"
fi

log "=== Auto-Heal Check Complete ==="
echo ""
