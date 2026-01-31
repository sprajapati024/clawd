#!/bin/bash
# Move all tasks from Clarke - Recurring Systems to Strategic (temporarily)

echo "Moving tasks from Clarke - Recurring Systems to Strategic..."

# Get task IDs from Clarke - Recurring Systems
tasks=$(todoist tasks -p "Clarke - Recurring Systems" | awk '{print $1}')

for task_id in $tasks; do
    echo "Moving task $task_id..."
    todoist move "$task_id" -p "Strategic"
    sleep 1  # Avoid rate limiting
done

echo "Done!"