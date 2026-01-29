#!/usr/bin/env python3
"""
Clarke's Gmail OAuth Authentication
Run this once to authorize Gmail read-only access
"""

import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path

# Read-only scope - cannot delete, send, or modify emails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

CREDS_FILE = Path.home() / '.clawdbot' / 'credentials' / 'google-gmail.json'
TOKEN_FILE = Path.home() / '.clawdbot' / 'credentials' / 'gmail-token.pickle'

def authenticate():
    """Authenticate and save token"""
    creds = None
    
    # Check if we already have a token
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        
        os.chmod(TOKEN_FILE, 0o600)
    
    print("✅ Gmail authentication successful!")
    print(f"   Token saved to: {TOKEN_FILE}")
    print("   Scope: READ-ONLY (cannot delete or send)")
    
    return creds

if __name__ == '__main__':
    authenticate()
