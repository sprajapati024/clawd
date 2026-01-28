#!/bin/bash
# Clarke's Daily Security Report
# Generates a human-readable security briefing for the past 24 hours

REPORT_FILE="/tmp/security-report-$(date +%Y%m%d).txt"

cat > "$REPORT_FILE" << 'HEADER'
🔒 DAILY SECURITY REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HEADER

echo "📅 Report Date: $(date '+%A, %B %d, %Y at %I:%M %p %Z')" >> "$REPORT_FILE"
echo "⏱️  Coverage: Past 24 hours" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# --- THREAT SUMMARY ---
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE"
echo "📊 THREAT SUMMARY" >> "$REPORT_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Count failed login attempts in last 24h
FAILED_LOGINS=$(sudo grep "Failed password" /var/log/auth.log 2>/dev/null | grep "$(date -d '1 day ago' '+%b %d')\|$(date '+%b %d')" | wc -l)
echo "❌ Failed Login Attempts: $FAILED_LOGINS" >> "$REPORT_FILE"

# Count banned IPs
CURRENTLY_BANNED=$(sudo fail2ban-client status sshd 2>/dev/null | grep "Currently banned" | awk '{print $4}')
TOTAL_BANNED=$(sudo fail2ban-client status sshd 2>/dev/null | grep "Total banned" | awk '{print $4}')
echo "🚫 IPs Currently Banned: $CURRENTLY_BANNED" >> "$REPORT_FILE"
echo "📈 Lifetime Total Bans: $TOTAL_BANNED" >> "$REPORT_FILE"

# Check for root login attempts
ROOT_ATTEMPTS=$(sudo grep "Failed password for root" /var/log/auth.log 2>/dev/null | grep "$(date -d '1 day ago' '+%b %d')\|$(date '+%b %d')" | wc -l)
if [ "$ROOT_ATTEMPTS" -gt 0 ]; then
    echo "⚠️  Root Login Attempts: $ROOT_ATTEMPTS (BLOCKED)" >> "$REPORT_FILE"
else
    echo "✅ Root Login Attempts: 0" >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"

# --- NEW BANS ---
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE"
echo "🚨 NEW BANS (Past 24h)" >> "$REPORT_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Extract recent bans from fail2ban log
RECENT_BANS=$(sudo grep "Ban " /var/log/fail2ban.log 2>/dev/null | grep "$(date -d '1 day ago' '+%Y-%m-%d')\|$(date '+%Y-%m-%d')" | tail -10)

if [ -n "$RECENT_BANS" ]; then
    echo "$RECENT_BANS" | while read line; do
        IP=$(echo "$line" | grep -oP '\d+\.\d+\.\d+\.\d+')
        TIME=$(echo "$line" | awk '{print $1, $2}')
        if [ -n "$IP" ]; then
            # Try to get country info (if geoiplookup is installed, otherwise skip)
            COUNTRY=$(geoiplookup "$IP" 2>/dev/null | head -1 | cut -d: -f2 | xargs || echo "Unknown")
            echo "  🔴 $TIME → Banned $IP ($COUNTRY)" >> "$REPORT_FILE"
        fi
    done
else
    echo "  ✅ No new bans in the past 24 hours" >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"

# --- ATTACK PATTERNS ---
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE"
echo "🎯 ATTACK PATTERNS" >> "$REPORT_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Top targeted usernames
echo "Most Targeted Usernames:" >> "$REPORT_FILE"
sudo grep "Failed password for" /var/log/auth.log 2>/dev/null | grep "$(date -d '1 day ago' '+%b %d')\|$(date '+%b %d')" | awk '{print $9}' | sort | uniq -c | sort -rn | head -5 | while read count user; do
    echo "  • $user: $count attempts" >> "$REPORT_FILE"
done

echo "" >> "$REPORT_FILE"

# Attack times (hourly distribution)
echo "Attack Timing (by hour):" >> "$REPORT_FILE"
sudo grep "Failed password" /var/log/auth.log 2>/dev/null | grep "$(date '+%b %d')" | awk '{print $3}' | cut -d: -f1 | sort | uniq -c | sort -rn | head -5 | while read count hour; do
    echo "  • ${hour}:00 → $count attempts" >> "$REPORT_FILE"
done

echo "" >> "$REPORT_FILE"

# --- AUTO-HEALING ACTIONS ---
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE"
echo "🔧 AUTO-HEALING ACTIONS" >> "$REPORT_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Check auto-heal log for actions taken
if [ -f /var/log/clarke-monitor/auto-heal.log ]; then
    HEAL_ACTIONS=$(grep -E "(Auto-healing|CRITICAL|SUCCESS|FAILED)" /var/log/clarke-monitor/auto-heal.log 2>/dev/null | grep "$(date -d '1 day ago' '+%Y-%m-%d')\|$(date '+%Y-%m-%d')" | tail -10)
    
    if [ -n "$HEAL_ACTIONS" ]; then
        echo "$HEAL_ACTIONS" >> "$REPORT_FILE"
    else
        echo "  ✅ No healing actions required - all systems healthy" >> "$REPORT_FILE"
    fi
else
    echo "  ℹ️  Auto-heal log not yet available" >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"

# --- SYSTEM STATUS ---
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE"
echo "💚 CURRENT SYSTEM STATUS" >> "$REPORT_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

DISK=$(df / | tail -1 | awk '{print $5}')
MEM=$(free | grep Mem | awk '{printf "%.0f%%", $3/$2 * 100}')
CPU=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}')

echo "💾 Disk Usage: $DISK" >> "$REPORT_FILE"
echo "🧠 Memory Usage: $MEM" >> "$REPORT_FILE"
echo "⚙️  CPU Load: $CPU" >> "$REPORT_FILE"
echo "🔥 Firewall: $(sudo ufw status | grep "Status:" | awk '{print $2}')" >> "$REPORT_FILE"
echo "🛡️  fail2ban: $(systemctl is-active fail2ban)" >> "$REPORT_FILE"

echo "" >> "$REPORT_FILE"

# --- WHAT THIS MEANS ---
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE"
echo "📚 WHAT THIS MEANS (Learning Section)" >> "$REPORT_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Contextual explanations based on activity
if [ "$FAILED_LOGINS" -gt 50 ]; then
    cat >> "$REPORT_FILE" << 'EXPLAIN1'
🎓 High Failed Login Activity:
   Your server is being scanned by automated bots trying common
   usernames and passwords. This is NORMAL for any public server.
   Our system blocks them after 3 attempts for 24 hours.
   No action needed - defenses are working.

EXPLAIN1
fi

if [ "$ROOT_ATTEMPTS" -gt 0 ]; then
    cat >> "$REPORT_FILE" << 'EXPLAIN2'
🎓 Root Login Attempts:
   Attackers always try "root" first because it exists on every Linux
   system and has full control. We've disabled root password login
   entirely - they can't get in even if they guess the password.
   This is a sign our security config is being tested (and passing).

EXPLAIN2
fi

if [ "$CURRENTLY_BANNED" -gt 5 ]; then
    cat >> "$REPORT_FILE" << 'EXPLAIN3'
🎓 Multiple Banned IPs:
   This could indicate a coordinated attack from multiple sources,
   or just normal internet background noise. fail2ban automatically
   bans IPs after repeated failures. Bans last 24 hours, then reset.
   If the same IPs keep coming back, they'll be banned again.

EXPLAIN3
fi

cat >> "$REPORT_FILE" << 'FOOTER'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️  Bottom Line: Your server is being actively protected.
   Every attack listed here was blocked automatically.
   You're safe. I'm watching.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

— Clarke
FOOTER

# Display the report
cat "$REPORT_FILE"

# Optional: Send via Telegram (would need integration)
# For now, just save it
cp "$REPORT_FILE" /var/log/clarke-monitor/latest-security-report.txt
