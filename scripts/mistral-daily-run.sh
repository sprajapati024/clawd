#!/bin/bash
# Daily Mistral pipeline execution for ROI data collection
# Ensures token usage logging for Feb 19 review

LOG_FILE="/var/log/clarke-monitor/mistral-daily-$(date +%Y%m%d).log"

echo "=== Mistral Daily Run: $(date) ===" >> "$LOG_FILE"

cd /root/clawd/scripts/mistral

# Run all 4 pipelines to collect token usage data
echo "Running email pipeline..." >> "$LOG_FILE"
python3 email_pipeline.py >> "$LOG_FILE" 2>&1

echo "Running security pipeline..." >> "$LOG_FILE"
python3 security_pipeline.py >> "$LOG_FILE" 2>&1

echo "Running memory pipeline..." >> "$LOG_FILE"
python3 memory_pipeline.py >> "$LOG_FILE" 2>&1

echo "Running finance pipeline (sample)..." >> "$LOG_FILE"
echo '[{"desc":"Sample transaction","amt":0}]' | python3 -c "import sys, json; from finance_pipeline import run; print(run(json.load(sys.stdin)))" >> "$LOG_FILE" 2>&1

echo "=== Completed: $(date) ===" >> "$LOG_FILE"

# Count total tokens logged today
TODAY=$(date +%Y-%m-%d)
TOKEN_COUNT=$(grep -c "\"ts\":" /root/clawd/scripts/mistral/token_log.jsonl 2>/dev/null || echo 0)
echo "Total token entries logged to date: $TOKEN_COUNT" >> "$LOG_FILE"
