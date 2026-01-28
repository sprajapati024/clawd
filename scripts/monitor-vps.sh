#!/bin/bash
# VPS Monitoring Script - Clarke's Watchdog

LOG_DIR="/var/log/clarke-monitor"
mkdir -p "$LOG_DIR"

DISK_THRESHOLD=80
MEMORY_THRESHOLD=85
CPU_THRESHOLD=90

# Check disk usage
check_disk() {
    usage=$(df / | awk 'NR==2 {print int($5)}')
    if [ $usage -gt $DISK_THRESHOLD ]; then
        echo "[ALERT] Disk usage: ${usage}%" >> "$LOG_DIR/alerts.log"
        return 1
    fi
    return 0
}

# Check memory usage
check_memory() {
    usage=$(free | awk 'NR==2 {printf("%.0f", $3/$2 * 100)}')
    if [ $usage -gt $MEMORY_THRESHOLD ]; then
        echo "[ALERT] Memory usage: ${usage}%" >> "$LOG_DIR/alerts.log"
        return 1
    fi
    return 0
}

# Check CPU usage (1 min average)
check_cpu() {
    usage=$(uptime | awk -F'load average:' '{print $2}' | awk '{print int($1)}')
    if [ $usage -gt $CPU_THRESHOLD ]; then
        echo "[ALERT] CPU load average: ${usage}%" >> "$LOG_DIR/alerts.log"
        return 1
    fi
    return 0
}

# Check if Clawdbot is running
check_clawdbot() {
    if ! pgrep -f "clawdbot" > /dev/null; then
        echo "[ALERT] Clawdbot process not found!" >> "$LOG_DIR/alerts.log"
        return 1
    fi
    return 0
}

# Check SSH security
check_ssh_security() {
    failed=$(grep "Failed password" /var/log/auth.log 2>/dev/null | wc -l)
    if [ $failed -gt 50 ]; then
        echo "[ALERT] High SSH failed login attempts: $failed" >> "$LOG_DIR/alerts.log"
        return 1
    fi
    return 0
}

# Log system health snapshot
log_health() {
    {
        echo "=== $(date) ==="
        echo "Disk: $(df -h / | awk 'NR==2 {print $5}')"
        echo "Memory: $(free -h | awk 'NR==2 {print $3 "/" $2}')"
        echo "Load: $(uptime | awk -F'load average:' '{print $2}')"
        echo "Processes: $(ps aux | wc -l)"
        echo ""
    } >> "$LOG_DIR/health.log"
}

# Main monitoring loop
main() {
    check_disk
    check_memory
    check_cpu
    check_clawdbot
    check_ssh_security
    log_health
}

main
