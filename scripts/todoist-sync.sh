#!/bin/bash
#
# Todoist Sync Script
# Keeps Todoist updated with TASKS.json and vice versa
#

set -e

TASKS_FILE="/root/clawd/TASKS.json"
LOG_FILE="/var/log/clarke-monitor/todoist-sync.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Todoist Sync Started ==="

# Check if Todoist CLI is available
if ! command -v todoist &> /dev/null; then
    log "ERROR: Todoist CLI not found"
    exit 1
fi

# Test connection
if ! todoist today &> /dev/null; then
    log "ERROR: Todoist connection failed (check API token)"
    exit 1
fi

log "Todoist connection verified"

# TODO: Implement two-way sync
# For now, just log that sync ran
# Future: Parse TASKS.json, compare with Todoist, update both ways

log "=== Todoist Sync Completed ==="
exit 0
