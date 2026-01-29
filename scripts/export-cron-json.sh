#!/bin/bash
# Export cron jobs to JSON for dashboard

OUTPUT_FILE="/root/clawd/CRON.json"

# Get cron list from clawdbot (this returns JSON already from our earlier call)
# Using a simple Node.js script to format it properly

cat > /tmp/export-cron.js << 'EOF'
const fs = require('fs');
const { execSync } = require('child_process');

// Only recurring tasks - no one-off projects
const jobs = [
  {
    name: 'morning-brief',
    schedule: '0 12 * * * (7 AM EST)',
    nextRun: 'Daily at 7:00 AM EST',
    enabled: true,
    description: '☀️ Morning Brief - Weather, security, system health'
  },
  {
    name: 'daily-security-report',
    schedule: '0 15 * * * (10 AM EST)',
    nextRun: 'Daily at 10:00 AM EST',
    enabled: true,
    description: '📊 Daily Security Report - 24hr threat summary'
  },
  {
    name: 'claude-ping-10am',
    schedule: '4 15 * * * (10:04 AM EST)',
    nextRun: 'Daily at 10:04 AM EST',
    enabled: true,
    description: '🔄 Claude Window Ping - Renew 5hr token window'
  },
  {
    name: 'journal-send',
    schedule: '30 17 * * * (12:30 PM EST)',
    nextRun: 'Daily at 12:30 PM EST',
    enabled: true,
    description: '📖 Lunch Journal Delivery - Daily reflection'
  },
  {
    name: 'claude-ping-3pm',
    schedule: '4 20 * * * (3:04 PM EST)',
    nextRun: 'Daily at 3:04 PM EST',
    enabled: true,
    description: '🔄 Claude Window Ping - Renew 5hr token window'
  },
  {
    name: 'claude-ping-8pm',
    schedule: '4 1 * * * (8:04 PM EST)',
    nextRun: 'Daily at 8:04 PM EST',
    enabled: true,
    description: '🔄 Claude Window Ping - Renew 5hr token window'
  },
  {
    name: 'gmail-scan',
    schedule: '0 6 * * * (1 AM EST)',
    nextRun: 'Daily at 1:00 AM EST',
    enabled: true,
    description: '📧 Gmail Scan - Inbox analysis & cleanup suggestions'
  },
  {
    name: 'claude-ping-1am',
    schedule: '4 6 * * * (1:04 AM EST)',
    nextRun: 'Daily at 1:04 AM EST',
    enabled: true,
    description: '🔄 Claude Window Ping - Renew 5hr token window'
  },
  {
    name: 'system-cleanup-logging',
    schedule: '30 7 * * * (2:30 AM EST)',
    nextRun: 'Daily at 2:30 AM EST',
    enabled: true,
    description: '🧹 System Cleanup - Fix logging, tune monitoring'
  },
  {
    name: 'journal-write',
    schedule: '0 8 * * * (3 AM EST)',
    nextRun: 'Daily at 3:00 AM EST',
    enabled: true,
    description: '📔 Journal Time - Daily reflection & introspection'
  },
  {
    name: 'claude-ping-6am',
    schedule: '4 11 * * * (6:04 AM EST)',
    nextRun: 'Daily at 6:04 AM EST',
    enabled: true,
    description: '🔄 Claude Window Ping - Renew 5hr token window'
  },
  {
    name: 'finance-weekly-summary',
    schedule: '0 13 * * 0 (8 AM EST Sunday)',
    nextRun: 'Sundays at 8:00 AM EST',
    enabled: true,
    description: '📊 Weekly Finance Summary - 7-day spending by category'
  },
  {
    name: 'build-fake-trader',
    schedule: '0 13 * * 0 (8 AM EST Sunday)',
    nextRun: 'Sundays at 8:00 AM EST',
    enabled: true,
    description: '🤖 Sub-Agent: Build Day Trading Simulator'
  },
  {
    name: 'monthly-review',
    schedule: '0 1 1 2 * (Jan 31 8 PM EST)',
    nextRun: 'Jan 31, 2026 at 8:00 PM EST',
    enabled: true,
    description: '🔔 Monthly Review - Performance check-in'
  },
  {
    name: 'finance-monthly-pdf',
    schedule: '0 14 27 * * (9 AM EST 27th)',
    nextRun: 'Monthly on 27th at 9:00 AM EST',
    enabled: true,
    description: '📈 Monthly Finance Report - Full PDF breakdown'
  }
];

const output = {
  meta: {
    lastUpdated: new Date().toISOString()
  },
  jobs: jobs
};

fs.writeFileSync('/root/clawd/CRON.json', JSON.stringify(output, null, 2));
console.log('✅ Cron jobs exported');
EOF

node /tmp/export-cron.js
