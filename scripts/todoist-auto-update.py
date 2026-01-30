#!/usr/bin/env python3
"""
Todoist Auto-Update Script
Automatically syncs tasks from various sources to Todoist
"""

import subprocess
import json
import os
from datetime import datetime

TASKS_FILE = "/root/clawd/TASKS.json"
LOG_FILE = "/var/log/clarke-monitor/todoist-updates.log"

def log(message):
    """Log message to file and stdout"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    with open(LOG_FILE, "a") as f:
        f.write(log_message + "\n")

def run_todoist_command(args):
    """Run todoist CLI command"""
    try:
        result = subprocess.run(
            ["todoist"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log(f"ERROR running todoist {' '.join(args)}: {e.stderr}")
        return None

def add_task_to_todoist(title, project=None, due=None, priority=None):
    """Add a task to Todoist"""
    args = ["add", title]
    
    if project:
        args.extend(["--project", project])
    if due:
        args.extend(["--due", due])
    if priority:
        args.extend(["--priority", str(priority)])
    
    result = run_todoist_command(args)
    if result:
        log(f"✅ Added task: {title}")
        return True
    return False

def update_from_tasks_json():
    """Update Todoist from TASKS.json"""
    if not os.path.exists(TASKS_FILE):
        log(f"TASKS.json not found at {TASKS_FILE}")
        return
    
    try:
        with open(TASKS_FILE, 'r') as f:
            tasks_data = json.load(f)
        
        log(f"Loaded TASKS.json (last updated: {tasks_data['meta']['lastUpdated']})")
        
        # Note: Full sync logic would go here
        # For now, this is a framework for future implementation
        
    except Exception as e:
        log(f"ERROR reading TASKS.json: {e}")

def main():
    log("=== Todoist Auto-Update Started ===")
    
    # Verify todoist CLI is available
    if subprocess.run(["which", "todoist"], capture_output=True).returncode != 0:
        log("ERROR: Todoist CLI not found")
        return 1
    
    # Test connection
    if run_todoist_command(["today"]) is None:
        log("ERROR: Todoist connection failed")
        return 1
    
    log("Todoist connection verified")
    
    # Update from TASKS.json
    update_from_tasks_json()
    
    log("=== Todoist Auto-Update Completed ===")
    return 0

if __name__ == "__main__":
    exit(main())
