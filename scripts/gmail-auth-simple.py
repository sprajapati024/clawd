#!/usr/bin/env python3
"""
Clarke's Gmail OAuth - Simple Auth Flow
Step 1: Generate authorization URL
Step 2: User authorizes in browser
Step 3: User provides the code
Step 4: Exchange code for token
"""

import os
import sys
import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDS_FILE = Path.home() / '.clawdbot' / 'credentials' / 'google-gmail.json'
TOKEN_FILE = Path.home() / '.clawdbot' / 'credentials' / 'gmail-token.pickle'

def main():
    if len(sys.argv) > 1:
        # Step 3: User provided the auth code
        auth_code = sys.argv[1]
        exchange_code_for_token(auth_code)
    else:
        # Step 1: Generate auth URL
        generate_auth_url()

def generate_auth_url():
    """Generate the authorization URL"""
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDS_FILE),
        SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # Out-of-band flow
    )
    
    auth_url, _ = flow.authorization_url(prompt='consent')
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📧 GMAIL AUTHORIZATION - STEP 1")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("")
    print("1. Open this URL in your browser:")
    print("")
    print(auth_url)
    print("")
    print("2. Sign in with your Gmail account")
    print("3. Grant READ-ONLY access (cannot delete or send)")
    print("4. Copy the authorization code")
    print("5. Run: python3 /root/clawd/scripts/gmail-auth-simple.py <CODE>")
    print("")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

def exchange_code_for_token(auth_code):
    """Exchange authorization code for access token"""
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDS_FILE),
        SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )
    
    try:
        flow.fetch_token(code=auth_code)
        creds = flow.credentials
        
        # Save token
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        
        os.chmod(TOKEN_FILE, 0o600)
        
        print("✅ Gmail authentication successful!")
        print(f"   Token saved to: {TOKEN_FILE}")
        print("   Scope: READ-ONLY")
        print("")
        print("You can now run: /root/clawd/scripts/gmail-scan.py")
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
