#!/bin/bash
# Clarke's Security Audit Script
# Runs automated security checks and reports anomalies

ALERT_LOG="/var/log/clarke-monitor/security-alerts.log"
mkdir -p "$(dirname "$ALERT_LOG")"

echo "=== Security Audit $(date) ===" >> "$ALERT_LOG"

# Check fail2ban status
BANNED_COUNT=$(sudo fail2ban-client status sshd | grep "Currently banned" | awk '{print $4}')
if [ "$BANNED_COUNT" -gt 5 ]; then
    echo "⚠️  HIGH THREAT: $BANNED_COUNT IPs currently banned" >> "$ALERT_LOG"
fi

# Check for new banned IPs since last run
TOTAL_BANNED=$(sudo fail2ban-client status sshd | grep "Total banned" | awk '{print $4}')
LAST_COUNT=$(cat /tmp/clarke-last-ban-count 2>/dev/null || echo 0)
if [ "$TOTAL_BANNED" -gt "$LAST_COUNT" ]; then
    NEW_BANS=$((TOTAL_BANNED - LAST_COUNT))
    echo "🚨 $NEW_BANS new IP(s) banned since last check" >> "$ALERT_LOG"
    sudo fail2ban-client status sshd | grep "Banned IP list" >> "$ALERT_LOG"
fi
echo "$TOTAL_BANNED" > /tmp/clarke-last-ban-count

# Check for suspicious auth attempts
RECENT_FAILS=$(sudo grep "Failed password" /var/log/auth.log 2>/dev/null | tail -10 | wc -l)
if [ "$RECENT_FAILS" -gt 20 ]; then
    echo "⚠️  $RECENT_FAILS recent failed password attempts" >> "$ALERT_LOG"
fi

# Check for root login attempts
ROOT_ATTEMPTS=$(sudo grep "Failed password for root" /var/log/auth.log 2>/dev/null | tail -1)
if [ -n "$ROOT_ATTEMPTS" ]; then
    echo "🔴 Root login attempt detected: $ROOT_ATTEMPTS" >> "$ALERT_LOG"
fi

# Check firewall status
UFW_STATUS=$(sudo ufw status | grep "Status:" | awk '{print $2}')
if [ "$UFW_STATUS" != "active" ]; then
    echo "🚨 CRITICAL: Firewall is NOT active!" >> "$ALERT_LOG"
fi

# Check for unauthorized SSH keys
AUTH_KEYS_COUNT=$(wc -l < /root/.ssh/authorized_keys 2>/dev/null || echo 0)
if [ "$AUTH_KEYS_COUNT" -gt 1 ]; then
    echo "⚠️  Multiple SSH keys detected ($AUTH_KEYS_COUNT total)" >> "$ALERT_LOG"
fi

echo "Audit complete." >> "$ALERT_LOG"
echo "" >> "$ALERT_LOG"
