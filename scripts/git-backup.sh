#!/bin/bash

# Daily git backup script
# Runs git add, commit, and push for the clawd repository

cd /root/clawd || exit 1

# Check if there are any changes
if git diff --quiet && git diff --cached --quiet; then
    echo "$(date): No changes to commit" >> /var/log/clarke-monitor/git-backup.log
    exit 0
fi

# Add all changes
git add -A

# Create commit with timestamp
commit_msg="Automated daily backup - $(date '+%Y-%m-%d %H:%M:%S %Z')"
if git commit -m "$commit_msg"; then
    # Push to origin
    if git push origin master; then
        echo "$(date): Successfully pushed backup" >> /var/log/clarke-monitor/git-backup.log
    else
        echo "$(date): Failed to push to origin" >> /var/log/clarke-monitor/git-backup.log
        exit 1
    fi
else
    echo "$(date): No changes to commit" >> /var/log/clarke-monitor/git-backup.log
fi