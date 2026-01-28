#!/bin/bash
# Clarke's Automated Backup System
# Backs up critical configuration and data

BACKUP_DIR="/root/backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="$BACKUP_DIR/clarke-backup-$TIMESTAMP.tar.gz"

mkdir -p "$BACKUP_DIR"

echo "🔄 Starting automated backup..."

# Create backup
tar -czf "$BACKUP_FILE" \
    -C / \
    root/clawd \
    etc/fail2ban/jail.local \
    etc/ssh/sshd_config \
    --exclude='root/clawd/node_modules' \
    --exclude='root/clawd/.git' \
    2>&1 | grep -v "Removing leading"

if [ $? -eq 0 ]; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "✅ Backup created: $BACKUP_FILE ($SIZE)"
    
    # Keep only last 7 backups
    cd "$BACKUP_DIR"
    ls -t clarke-backup-*.tar.gz | tail -n +8 | xargs -r rm
    
    REMAINING=$(ls -1 clarke-backup-*.tar.gz 2>/dev/null | wc -l)
    echo "📦 Total backups kept: $REMAINING"
else
    echo "❌ Backup failed!"
    exit 1
fi
