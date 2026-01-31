#!/usr/bin/env python3
"""
Heartbeat Dispatcher - Scans Todoist for eligible tasks and acts
"""

from todoist_api_python.api import TodoistAPI
from datetime import datetime, timezone, timedelta, date
from dateutil import parser as date_parser
import sys
import json

TOKEN = "0dace15d68887c208ec6bd9de883d4356c9a7fe9"

def scan_and_act():
    """Scan Todoist for eligible tasks and return list of actions needed"""
    
    api = TodoistAPI(TOKEN)
    
    # Get current time
    now_utc = datetime.now(timezone.utc)
    
    # Get all tasks - the paginator returns lists
    all_tasks = []
    for batch in api.get_tasks():
        # Each batch is a list of tasks
        if isinstance(batch, list):
            all_tasks.extend(batch)
        else:
            all_tasks.append(batch)
    
    eligible_tasks = []
    
    for task in all_tasks:
        if not hasattr(task, 'due') or not task.due:
            continue
        
        # Parse due time from Due object
        due_value = task.due.date  # This is datetime.date or datetime.datetime
        try:
            if isinstance(due_value, datetime):
                due_dt = due_value
            elif isinstance(due_value, date):
                # Convert date to datetime at start of day
                due_dt = datetime.combine(due_value, datetime.min.time())
            else:
                due_dt = date_parser.parse(str(due_value))
            
            # Make timezone aware
            if due_dt.tzinfo is None:
                due_dt = due_dt.replace(tzinfo=timezone.utc)
        except:
            continue
        
        # Check if due
        if now_utc < due_dt:
            continue  # Not yet due
        
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
        for comment in comments:
            if hasattr(comment, 'content') and 'Status:' in comment.content:
                if 'Done' in comment.content or 'In progress' in comment.content or 'Blocked' in comment.content:
                    status = 'skip'
                    break
                elif 'Ready' in comment.content:
                    status = 'ready'
                elif 'Needs clarity' in comment.content:
                    status = 'needs_clarity'
        
        if status in ['ready', 'needs_clarity']:
            eligible_tasks.append({
                'id': task.id,
                'content': task.content,
                'status': status,
                'due': due_dt.strftime('%Y-%m-%d %H:%M'),
                'project_id': task.project_id
            })
    
    return eligible_tasks

if __name__ == '__main__':
    try:
        tasks = scan_and_act()
        
        # Output JSON for programmatic use
        print(json.dumps({
            'eligible_count': len(tasks),
            'tasks': tasks
        }, indent=2))
        
    except Exception as e:
        print(json.dumps({
            'error': str(e),
            'eligible_count': 0,
            'tasks': []
        }))
        import traceback
        traceback.print_exc()
        sys.exit(1)
