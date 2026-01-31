#!/usr/bin/env python3
"""
Clarke's Gmail Important Scanner
Scans for events, bills, and important notifications
"""

import pickle
import sys
import re
from pathlib import Path
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from dateutil import parser as date_parser

TOKEN_FILE = Path.home() / '.clawdbot' / 'credentials' / 'gmail-token.pickle'

def load_credentials():
    """Load saved credentials"""
    if not TOKEN_FILE.exists():
        print("❌ Not authenticated yet. Run: /root/clawd/scripts/gmail-auth.py")
        sys.exit(1)
    
    with open(TOKEN_FILE, 'rb') as token:
        return pickle.load(token)

def extract_events(subject, snippet, from_email):
    """Detect if email contains event information"""
    event_keywords = [
        'invitation', 'invite', 'meeting', 'calendar', 'event',
        'rsvp', 'attending', 'join us', 'save the date',
        'reminder:', 'starts in', 'happening', 'scheduled'
    ]
    
    text = (subject + ' ' + snippet).lower()
    
    # Check for event keywords
    if any(keyword in text for keyword in event_keywords):
        return True
    
    # Check for calendar-related domains
    calendar_domains = ['calendar', 'eventbrite', 'meetup', 'zoom', 'teams']
    if any(domain in from_email.lower() for domain in calendar_domains):
        return True
    
    return False

def extract_bills(subject, snippet, from_email):
    """Detect if email contains bill/payment information"""
    bill_keywords = [
        'bill', 'invoice', 'payment', 'due', 'overdue',
        'statement', 'balance', 'charge', 'receipt',
        'subscription', 'renewal', 'autopay', 'transaction'
    ]
    
    text = (subject + ' ' + snippet).lower()
    
    # Check for bill keywords
    if any(keyword in text for keyword in bill_keywords):
        return True
    
    # Check for financial domains
    financial_domains = ['bank', 'paypal', 'stripe', 'bill', 'payment', 'credit']
    if any(domain in from_email.lower() for domain in financial_domains):
        return True
    
    return False

def extract_important_notifications(subject, snippet, from_email):
    """Detect important notifications"""
    important_keywords = [
        'urgent', 'important', 'action required', 'verify',
        'confirm', 'security', 'alert', 'warning',
        'expires', 'expiring', 'deadline', 'final notice'
    ]
    
    text = (subject + ' ' + snippet).lower()
    
    # Check for important keywords
    if any(keyword in text for keyword in important_keywords):
        return True
    
    return False

def scan_recent_emails(days_back=7, max_results=100):
    """Scan recent emails for important items"""
    creds = load_credentials()
    service = build('gmail', 'v1', credentials=creds)
    
    # Calculate date range
    after_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y/%m/%d')
    
    # Search for unread or recent important emails
    query = f'after:{after_date} (is:unread OR is:important)'
    
    results = service.users().messages().list(
        userId='me',
        maxResults=max_results,
        q=query
    ).execute()
    
    messages = results.get('messages', [])
    
    if not messages:
        return {
            'events': [],
            'bills': [],
            'important': []
        }
    
    events = []
    bills = []
    important = []
    
    for msg in messages:
        msg_data = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='full'
        ).execute()
        
        headers = {h['name']: h['value'] for h in msg_data['payload']['headers']}
        subject = headers.get('Subject', '(no subject)')
        from_email = headers.get('From', '')
        date_str = headers.get('Date', '')
        snippet = msg_data.get('snippet', '')
        
        # Extract sender
        if '<' in from_email:
            sender_name = from_email.split('<')[0].strip()
            sender_email = from_email.split('<')[1].split('>')[0]
        else:
            sender_name = from_email
            sender_email = from_email
        
        # Parse date
        try:
            email_date = date_parser.parse(date_str)
        except:
            email_date = datetime.now()
        
        email_info = {
            'subject': subject,
            'from_name': sender_name,
            'from_email': sender_email,
            'date': email_date,
            'snippet': snippet,
            'id': msg['id']
        }
        
        # Categorize
        if extract_events(subject, snippet, from_email):
            events.append(email_info)
        elif extract_bills(subject, snippet, from_email):
            bills.append(email_info)
        elif extract_important_notifications(subject, snippet, from_email):
            important.append(email_info)
    
    return {
        'events': events,
        'bills': bills,
        'important': important
    }

def format_for_telegram(scan_results):
    """Format scan results for Telegram delivery"""
    events = scan_results['events']
    bills = scan_results['bills']
    important = scan_results['important']
    
    if not events and not bills and not important:
        return None
    
    message = "📧 **Gmail Scanner Report**\n\n"
    
    if events:
        message += "📅 **Events & Meetings:**\n"
        for event in events[:5]:  # Limit to 5
            date_str = event['date'].strftime('%b %d')
            message += f"  • {event['subject']}\n"
            message += f"    From: {event['from_name']} ({date_str})\n\n"
    
    if bills:
        message += "💳 **Bills & Payments:**\n"
        for bill in bills[:5]:
            date_str = bill['date'].strftime('%b %d')
            message += f"  • {bill['subject']}\n"
            message += f"    From: {bill['from_name']} ({date_str})\n\n"
    
    if important:
        message += "⚠️ **Important Notifications:**\n"
        for item in important[:5]:
            date_str = item['date'].strftime('%b %d')
            message += f"  • {item['subject']}\n"
            message += f"    From: {item['from_name']} ({date_str})\n\n"
    
    return message

def main():
    """Main scanner function"""
    print("🔍 Scanning Gmail for important items...")
    
    results = scan_recent_emails(days_back=7)
    
    total = len(results['events']) + len(results['bills']) + len(results['important'])
    
    if total == 0:
        print("✅ No important items found in recent emails")
        return None
    
    print(f"📊 Found {total} important items:")
    print(f"  📅 Events: {len(results['events'])}")
    print(f"  💳 Bills: {len(results['bills'])}")
    print(f"  ⚠️ Important: {len(results['important'])}")
    print("")
    
    telegram_message = format_for_telegram(results)
    
    if telegram_message:
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(telegram_message)
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    return telegram_message

if __name__ == '__main__':
    main()
