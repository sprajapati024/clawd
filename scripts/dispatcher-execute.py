#!/usr/bin/env python3
"""
Todoist Dispatcher - Runs hourly, spawns agents for eligible tasks
"""

from todoist_api_python.api import TodoistAPI
from datetime import datetime, timezone, date
from dateutil import parser as date_parser
import sys
import json
import subprocess
import os

TOKEN = "0dace15d68887c208ec6bd9de883d4356c9a7fe9"

def scan_eligible_tasks():
    """Scan Todoist for eligible tasks"""
    
    api = TodoistAPI(TOKEN)
    now_utc = datetime.now(timezone.utc)
    
    # Get all tasks
    all_tasks = []
    for batch in api.get_tasks():
        if isinstance(batch, list):
            all_tasks.extend(batch)
        else:
            all_tasks.append(batch)
    
    eligible_tasks = []
    
    for task in all_tasks:
        if not hasattr(task, 'due') or not task.due:
            continue
        
        # Parse due time
        due_value = task.due.date
        try:
            if isinstance(due_value, datetime):
                due_dt = due_value
            elif isinstance(due_value, date):
                due_dt = datetime.combine(due_value, datetime.min.time())
            else:
                due_dt = date_parser.parse(str(due_value))
            
            if due_dt.tzinfo is None:
                due_dt = due_dt.replace(tzinfo=timezone.utc)
        except:
            continue
        
        # Check if due
        if now_utc < due_dt:
            continue
        
        # Check status via comments
        try:
            comments_batch = api.get_comments(task_id=task.id)
            comments = []
            for comment_item in comments_batch:
                if isinstance(comment_item, list):
                    comments.extend(comment_item)
                else:
                    comments.append(comment_item)
        except:
            comments = []
        
        status = None
        assigned_to = None
        
        for comment in comments:
            if hasattr(comment, 'content'):
                if 'Status:' in comment.content:
                    if 'Done' in comment.content or 'In progress' in comment.content or 'Blocked' in comment.content:
                        status = 'skip'
                        break
                    elif 'Ready' in comment.content:
                        status = 'ready'
                    elif 'Needs clarity' in comment.content:
                        status = 'needs_clarity'
                
                # Extract assigned agent from comments
                if '@Forge' in comment.content or '@forge' in comment.content:
                    assigned_to = 'forge'
                elif '@Atlas' in comment.content or '@atlas' in comment.content:
                    assigned_to = 'atlas'
        
        if status in ['ready', 'needs_clarity']:
            eligible_tasks.append({
                'id': task.id,
                'content': task.content,
                'status': status,
                'assigned_to': assigned_to,
                'due': due_dt.strftime('%Y-%m-%d %H:%M')
            })
    
    return eligible_tasks

def execute_task(task):
    """Execute a single task by spawning appropriate agent or asking for clarity"""
    
    task_id = task['id']
    content = task['content']
    status = task['status']
    assigned_to = task['assigned_to']
    
    # Build message to send to Telegram
    if status == 'needs_clarity':
        # Ask Shirin for clarification
        message = f"🚦 **Task needs clarification:**\n\n{content}\n\n(Task ID: {task_id})"
        
        # Send via clawdbot message tool would go here
        # For now, just output
        print(f"NEEDS_CLARITY: {content}")
        return {'action': 'asked_for_clarity', 'task': content}
    
    elif status == 'ready':
        # Mark as In progress first
        api = TodoistAPI(TOKEN)
        api.add_comment(
            task_id=task_id,
            content=f"Status: In progress — Dispatcher started work at {datetime.now().strftime('%H:%M EST')}"
        )
        
        # Spawn agent or execute work
        print(f"EXECUTING: {content} (assigned to: {assigned_to})")
        
        # This is where we'd spawn the agent
        # For now, return intent
        return {
            'action': 'started_work',
            'task': content,
            'assigned_to': assigned_to,
            'task_id': task_id
        }

def main():
    """Main dispatcher loop"""
    
    tasks = scan_eligible_tasks()
    
    if not tasks:
        # Silent exit - nothing to do
        sys.exit(0)
    
    print(f"🚦 Dispatcher found {len(tasks)} eligible tasks")
    print()
    
    results = []
    for task in tasks:
        result = execute_task(task)
        results.append(result)
    
    # Output results as JSON
    print()
    print(json.dumps(results, indent=2))
    
    # Return non-zero if work was started (signals to send notification)
    if results:
        sys.exit(1)  # Signal: work happened, notify user

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"❌ Dispatcher error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)
