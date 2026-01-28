#!/usr/bin/env python3
"""
Ultrahuman Ring Data Fetcher
Pulls yesterday's health data from Ultrahuman Ring API
Formats it for daily morning briefing
"""

import requests
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Config
ULTRAHUMAN_API_BASE = "https://partner.ultrahuman.com"
CONFIG_FILE = Path.home() / ".clawd" / "ultrahuman_config.json"
DATA_FILE = Path.home() / ".clawd" / "ultrahuman_data.json"

class UltrahumanClient:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = None
        
    def save_config(self):
        """Save credentials securely (for later use after OAuth)"""
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        config = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "token_expiry": self.token_expiry
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
        # Secure permissions
        os.chmod(CONFIG_FILE, 0o600)
    
    def load_config(self):
        """Load saved tokens"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                self.access_token = config.get("access_token")
                self.refresh_token = config.get("refresh_token")
                self.token_expiry = config.get("token_expiry")
                return True
        return False
    
    def refresh_access_token(self):
        """Refresh expired access token"""
        if not self.refresh_token:
            raise Exception("No refresh token available")
        
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        response = requests.post(f"{ULTRAHUMAN_API_BASE}/oauth/token", json=payload)
        response.raise_for_status()
        
        data = response.json()
        self.access_token = data["access_token"]
        self.refresh_token = data.get("refresh_token", self.refresh_token)
        self.token_expiry = datetime.now() + timedelta(days=7)
        
        self.save_config()
        return True
    
    def get_headers(self):
        """Get auth headers for API calls"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def fetch_ring_data(self, date_str):
        """Fetch ring data for a specific date (YYYY-MM-DD)"""
        headers = self.get_headers()
        url = f"{ULTRAHUMAN_API_BASE}/api/v1/ring/daily"
        params = {"date": date_str}
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def fetch_recovery_index(self, date_str):
        """Fetch recovery metrics for a date"""
        headers = self.get_headers()
        url = f"{ULTRAHUMAN_API_BASE}/api/v1/ring/recovery"
        params = {"date": date_str}
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()

def format_brief(ring_data, recovery_data, date_str):
    """Format health data into readable brief"""
    brief = f"🏥 **Health Brief - {date_str}**\n\n"
    
    # Sleep
    if "sleep" in ring_data:
        sleep = ring_data["sleep"]
        brief += f"😴 **Sleep:** {sleep.get('duration', 'N/A')} hours\n"
        if sleep.get("quality"):
            brief += f"   Quality: {sleep['quality']}\n"
    
    # Heart Rate
    if "heart_rate" in ring_data:
        hr = ring_data["heart_rate"]
        brief += f"❤️ **Heart Rate:** {hr.get('average', 'N/A')} bpm (avg)\n"
        if hr.get("resting"):
            brief += f"   Resting: {hr['resting']} bpm\n"
    
    # HRV
    if "hrv" in ring_data:
        brief += f"📊 **HRV:** {ring_data['hrv'].get('average', 'N/A')}\n"
    
    # Temperature
    if "temperature" in ring_data:
        brief += f"🌡️ **Temperature:** {ring_data['temperature'].get('average', 'N/A')}°C\n"
    
    # Recovery
    if recovery_data and "recovery_index" in recovery_data:
        brief += f"⚡ **Recovery Index:** {recovery_data['recovery_index']}\n"
    
    if recovery_data and "movement_index" in recovery_data:
        brief += f"🏃 **Movement Index:** {recovery_data['movement_index']}\n"
    
    # VO2 Max
    if "vo2_max" in ring_data:
        brief += f"💨 **VO2 Max:** {ring_data['vo2_max'].get('value', 'N/A')}\n"
    
    brief += "\n---\n"
    return brief

def main():
    # Load config if it exists
    client = UltrahumanClient(
        client_id=os.getenv("ULTRAHUMAN_CLIENT_ID"),
        client_secret=os.getenv("ULTRAHUMAN_CLIENT_SECRET"),
        redirect_uri=os.getenv("ULTRAHUMAN_REDIRECT_URI", "http://localhost:8000/callback")
    )
    
    # Check if we have saved tokens
    if not client.load_config():
        print("❌ No Ultrahuman credentials found.")
        print("Setup required:")
        print("1. Set env vars: ULTRAHUMAN_CLIENT_ID, ULTRAHUMAN_CLIENT_SECRET")
        print("2. Complete OAuth flow (manual for now)")
        return
    
    # Refresh token if needed
    if client.token_expiry and datetime.fromisoformat(client.token_expiry) < datetime.now():
        print("🔄 Refreshing access token...")
        client.refresh_access_token()
    
    # Fetch yesterday's data
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    try:
        print(f"📡 Fetching Ultrahuman data for {yesterday}...")
        ring_data = client.fetch_ring_data(yesterday)
        recovery_data = client.fetch_recovery_index(yesterday)
        
        # Format brief
        brief = format_brief(ring_data, recovery_data, yesterday)
        print(brief)
        
        # Save to file for integration with other systems
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump({
                "date": yesterday,
                "ring_data": ring_data,
                "recovery_data": recovery_data,
                "brief": brief,
                "fetched_at": datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"✅ Data saved to {DATA_FILE}")
        
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
