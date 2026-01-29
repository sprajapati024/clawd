#!/usr/bin/env python3
"""
Clarke's Gmail Inbox Scanner (Read-Only)
Analyzes inbox and suggests cleanup actions
"""

import pickle
import sys
from pathlib import Path
from googleapiclient.discovery import build
from collections import defaultdict
from datetime import datetime, timedelta

TOKEN_FILE = Path.home() / '.clawdbot' / 'credentials' / 'gmail-token.pickle'

def load_credentials():
    """Load saved credentials"""
    if not TOKEN_FILE.exists():
        print("❌ Not authenticated yet. Run: /root/clawd/scripts/gmail-auth.py")
        sys.exit(1)
    
    with open(TOKEN_FILE, 'rb') as token:
        return pickle.load(token)

def scan_inbox(max_results=500):
    """Scan inbox and categorize emails"""
    creds = load_credentials()
    service = build('gmail', 'v1', credentials=creds)
    
    print("📧 Scanning Gmail inbox...")
    print("")
    
    # Get messages
    results = service.users().messages().list(
        userId='me',
        maxResults=max_results,
        q='in:inbox'
    ).execute()
    
    messages = results.get('messages', [])
    
    if not messages:
        print("✅ Inbox is empty!")
        return
    
    print(f"📊 Found {len(messages)} emails in inbox")
    print("")
    
    # Categorize by sender domain
    by_domain = defaultdict(list)
    by_label = defaultdict(list)
    unread_count = 0
    old_count = 0  # > 30 days
    
    cutoff_date = datetime.now() - timedelta(days=30)
    
    for msg in messages[:100]:  # Analyze first 100 in detail
        msg_data = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata',
            metadataHeaders=['From', 'Subject', 'Date']
        ).execute()
        
        headers = {h['name']: h['value'] for h in msg_data['payload']['headers']}
        labels = msg_data.get('labelIds', [])
        
        # Extract sender domain
        from_header = headers.get('From', '')
        if '<' in from_header:
            email = from_header.split('<')[1].split('>')[0]
        else:
            email = from_header
        
        domain = email.split('@')[-1] if '@' in email else 'unknown'
        
        by_domain[domain].append({
            'id': msg['id'],
            'subject': headers.get('Subject', '(no subject)'),
            'from': from_header,
            'date': headers.get('Date', ''),
            'labels': labels
        })
        
        if 'UNREAD' in labels:
            unread_count += 1
        
        # Check if old
        try:
            msg_date = datetime.strptime(headers.get('Date', ''), '%a, %d %b %Y %H:%M:%S %z')
            if msg_date.replace(tzinfo=None) < cutoff_date:
                old_count += 1
        except:
            pass
    
    # Report findings
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📈 INBOX ANALYSIS")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("")
    print(f"  📬 Total in inbox: {len(messages)}")
    print(f"  ✉️  Unread: {unread_count}")
    print(f"  📅 Older than 30 days: {old_count}")
    print("")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("TOP SENDERS (by domain)")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("")
    
    sorted_domains = sorted(by_domain.items(), key=lambda x: len(x[1]), reverse=True)
    
    for domain, emails in sorted_domains[:15]:
        print(f"  {domain:40} {len(emails):3} emails")
        
        # Show a few subjects from this domain
        for email in emails[:2]:
            subject = email['subject'][:50] + '...' if len(email['subject']) > 50 else email['subject']
            print(f"    └─ {subject}")
    
    print("")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("💡 CLEANUP SUGGESTIONS")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("")
    
    # Suggest cleanup
    promotional_domains = []
    for domain, emails in sorted_domains:
        if any(keyword in domain.lower() for keyword in ['marketing', 'news', 'promo', 'deals', 'offers', 'newsletter']):
            promotional_domains.append((domain, len(emails)))
    
    if promotional_domains:
        total_promo = sum(count for _, count in promotional_domains)
        print(f"  📢 Promotional emails: ~{total_promo}")
        print("     (newsletters, marketing, deals)")
        print("")
    
    if old_count > 50:
        print(f"  🗂️  Archive old emails: {old_count} emails older than 30 days")
        print("     Consider archiving to clean up inbox")
        print("")
    
    if unread_count > 20:
        print(f"  👀 Unread backlog: {unread_count} unread emails")
        print("     Mark as read or archive?")
        print("")
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("")
    print("ℹ️  This is READ-ONLY analysis. I cannot delete or modify emails.")
    print("   Tell me what you want to clean up and I'll suggest filters/actions.")

if __name__ == '__main__':
    scan_inbox()
