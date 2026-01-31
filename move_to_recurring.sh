#!/bin/bash
# Move recurring tasks from Strategic to Recurring project

echo "Moving recurring tasks from Strategic to Recurring..."

# Task IDs of recurring tasks (from above output)
recurring_tasks=(
  "6fv38MCMRx3q6fPw"   # Claude Window Ping - 3 PM
  "6fv38MJMgpPF95vP"   # Claude Window Ping - 8 PM
  "6fv38MQ2FRVh3CfP"   # Claude Window Ping - 1 AM
  "6fv38MgMXCMr2hvP"   # Claude Window Ping - 6 AM
  "6fv38Mr7qH8jmpjw"   # Claude Window Ping - 10 AM
  "6fv38P5GGggV82XP"   # Daily Git Backup
  "6fv38P98CGvCwj7P"   # Journal Writing
  "6fv38PM7rfF4Hj8w"   # Improvement Analysis
  "6fv38PPQ2hj28gpP"   # Morning Brief
  "6fv38PgVmrXxWHcw"   # Journal Delivery
  "6fv38Pm46h6Xrqww"   # Weekly Finance Summary
  "6fv38Prpw56f5mqP"   # Monthly Review
  "6fv38Q4w2GMpf9qw"   # Monthly Finance PDF
)

for task_id in "${recurring_tasks[@]}"; do
    echo "Moving task $task_id to Recurring..."
    todoist move "$task_id" -p "Recurring"
    sleep 1  # Avoid rate limiting
done

echo "Done!"