#!/usr/bin/env python3
"""
Clarke's Gmail Full Inbox Scanner
Gets the actual total count
"""

import pickle
import sys
from pathlib import Path
from googleapiclient.discovery import build

TOKEN_FILE = Path.home() / '.clawdbot' / 'credentials' / 'gmail-token.pickle'

def load_credentials():
    if not TOKEN_FILE.exists():
        print("❌ Not authenticated yet.")
        sys.exit(1)
    
    with open(TOKEN_FILE, 'rb') as token:
        return pickle.load(token)

def get_full_count():
    creds = load_credentials()
    service = build('gmail', 'v1', credentials=creds)
    
    # Get all inbox messages (just IDs, no content)
    all_messages = []
    page_token = None
    
    print("📧 Counting all emails in inbox...")
    
    while True:
        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            pageToken=page_token
        ).execute()
        
        messages = results.get('messages', [])
        all_messages.extend(messages)
        
        page_token = results.get('nextPageToken')
        
        print(f"   Found {len(all_messages)} so far...")
        
        if not page_token:
            break
    
    print("")
    print(f"📊 TOTAL IN INBOX: {len(all_messages)} emails")
    
    # Get unread count
    unread_results = service.users().messages().list(
        userId='me',
        labelIds=['INBOX', 'UNREAD']
    ).execute()
    
    unread_count = unread_results.get('resultSizeEstimate', 0)
    
    print(f"✉️  UNREAD: {unread_count} emails")
    
    return len(all_messages), unread_count

if __name__ == '__main__':
    get_full_count()
