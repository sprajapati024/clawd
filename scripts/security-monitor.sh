#!/bin/bash
# Security Monitor Script - Runs during heartbeats to check for attacks

LOG_FILE="/var/log/clarke-monitor/security.log"
ALERT_FILE="/var/log/clarke-monitor/alerts.log"
FAIL2BAN_STATUS="/tmp/fail2ban-status.txt"

# Create log directory if needed
mkdir -p /var/log/clarke-monitor/

echo "=== SECURITY MONITOR $(date) ===" | tee -a "$LOG_FILE"

# 1. Check SSH attack attempts
SSH_ATTEMPTS=$(sudo grep -c "Failed password" /var/log/auth.log 2>/dev/null || echo "0")
SSH_LAST_24H=$(sudo grep "Failed password" /var/log/auth.log 2>/dev/null | grep "$(date -d '24 hours ago' '+%Y-%m-%d')" | wc -l)

echo "SSH Failed attempts:" | tee -a "$LOG_FILE"
echo "  Total: $SSH_ATTEMPTS" | tee -a "$LOG_FILE"
echo "  Last 24h: $SSH_LAST_24H" | tee -a "$LOG_FILE"

# 2. Check fail2ban status
sudo fail2ban-client status sshd > "$FAIL2BAN_STATUS" 2>/dev/null
CURRENTLY_BANNED=$(grep "Currently banned" "$FAIL2BAN_STATUS" | awk '{print $4}')
TOTAL_BANNED=$(grep "Total banned" "$FAIL2BAN_STATUS" | awk '{print $4}')

echo "Fail2Ban Status:" | tee -a "$LOG_FILE"
echo "  Currently banned: $CURRENTLY_BANNED" | tee -a "$LOG_FILE"
echo "  Total banned: $TOTAL_BANNED" | tee -a "$LOG_FILE"

# 3. Check firewall blocked IPs
UFW_BLOCKED=$(sudo ufw status numbered | grep -c "DENY IN")
echo "Firewall blocked IPs: $UFW_BLOCKED" | tee -a "$LOG_FILE"

# 4. Alert thresholds
if [ "$SSH_LAST_24H" -gt 50 ]; then
  echo "[ALERT] High SSH failed login attempts: $SSH_LAST_24H" | tee -a "$ALERT_FILE"
fi

if [ "$CURRENTLY_BANNED" -gt 10 ]; then
  echo "[ALERT] High number of banned IPs: $CURRENTLY_BANNED" | tee -a "$ALERT_FILE"
fi

# 5. Show recent attacks (last 5)
echo "" | tee -a "$LOG_FILE"
echo "Recent attack attempts (last 5):" | tee -a "$LOG_FILE"
sudo grep "Failed password" /var/log/auth.log 2>/dev/null | tail -5 | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "=== END SECURITY MONITOR ===" | tee -a "$LOG_FILE"