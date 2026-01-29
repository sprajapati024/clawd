#!/usr/bin/env python3
"""
Token usage tracker for Mistral (local) vs Claude (API)
Tracks daily usage and calculates cost savings
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Pricing (approximate)
CLAUDE_COST_PER_1K_TOKENS = 0.025  # Claude Sonnet pricing estimate
MISTRAL_COST_PER_1K_TOKENS = 0.0    # Local = free

TRACKER_FILE = "/root/clawd/data/token-usage.json"

def ensure_data_dir():
    """Create data directory if it doesn't exist"""
    Path("/root/clawd/data").mkdir(parents=True, exist_ok=True)

def load_tracker():
    """Load token tracking data"""
    ensure_data_dir()
    if not os.path.exists(TRACKER_FILE):
        return {"daily": {}, "total": {"mistral": 0, "claude": 0}}
    with open(TRACKER_FILE, 'r') as f:
        return json.load(f)

def save_tracker(data):
    """Save token tracking data"""
    ensure_data_dir()
    with open(TRACKER_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def log_tokens(source, tokens, operation=""):
    """
    Log token usage
    source: 'mistral' or 'claude'
    tokens: int
    operation: optional description
    """
    data = load_tracker()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today not in data["daily"]:
        data["daily"][today] = {"mistral": 0, "claude": 0, "operations": []}
    
    data["daily"][today][source] += tokens
    data["total"][source] += tokens
    
    if operation:
        data["daily"][today]["operations"].append({
            "time": datetime.now().isoformat(),
            "source": source,
            "tokens": tokens,
            "operation": operation
        })
    
    save_tracker(data)
    return data

def get_daily_stats(date=None):
    """Get stats for a specific date (default: today)"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    data = load_tracker()
    if date not in data["daily"]:
        return {"mistral": 0, "claude": 0, "savings": 0, "savings_pct": 0}
    
    day_data = data["daily"][date]
    mistral_tokens = day_data.get("mistral", 0)
    claude_tokens = day_data.get("claude", 0)
    
    # Calculate what it WOULD cost if all tokens were Claude
    total_tokens = mistral_tokens + claude_tokens
    claude_only_cost = (total_tokens / 1000) * CLAUDE_COST_PER_1K_TOKENS
    actual_cost = (claude_tokens / 1000) * CLAUDE_COST_PER_1K_TOKENS
    savings = claude_only_cost - actual_cost
    savings_pct = (mistral_tokens / total_tokens * 100) if total_tokens > 0 else 0
    
    return {
        "mistral": mistral_tokens,
        "claude": claude_tokens,
        "total": total_tokens,
        "actual_cost": actual_cost,
        "claude_only_cost": claude_only_cost,
        "savings": savings,
        "savings_pct": savings_pct
    }

def get_total_stats():
    """Get cumulative stats"""
    data = load_tracker()
    mistral_total = data["total"].get("mistral", 0)
    claude_total = data["total"].get("claude", 0)
    
    total_tokens = mistral_total + claude_total
    claude_only_cost = (total_tokens / 1000) * CLAUDE_COST_PER_1K_TOKENS
    actual_cost = (claude_total / 1000) * CLAUDE_COST_PER_1K_TOKENS
    savings = claude_only_cost - actual_cost
    savings_pct = (mistral_total / total_tokens * 100) if total_tokens > 0 else 0
    
    return {
        "mistral": mistral_total,
        "claude": claude_total,
        "total": total_tokens,
        "actual_cost": actual_cost,
        "claude_only_cost": claude_only_cost,
        "savings": savings,
        "savings_pct": savings_pct
    }

def format_brief():
    """Format token stats for morning brief"""
    daily = get_daily_stats()
    
    if daily["total"] == 0:
        return "📊 Token Usage (24h): No usage yet today"
    
    output = f"""📊 Token Usage (24h):
• Local (Mistral): {daily['mistral']:,} tokens ($0.00)
• Claude API: {daily['claude']:,} tokens (${daily['actual_cost']:.2f})
• Optimization: {daily['savings_pct']:.1f}% reduction (${daily['savings']:.2f} saved)"""
    
    return output

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print(format_brief())
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "log":
        if len(sys.argv) < 4:
            print("Usage: token-tracker.py log <mistral|claude> <tokens> [operation]")
            sys.exit(1)
        source = sys.argv[2]
        tokens = int(sys.argv[3])
        operation = sys.argv[4] if len(sys.argv) > 4 else ""
        log_tokens(source, tokens, operation)
        print(f"Logged {tokens} tokens for {source}")
    
    elif command == "daily":
        stats = get_daily_stats()
        print(json.dumps(stats, indent=2))
    
    elif command == "total":
        stats = get_total_stats()
        print(json.dumps(stats, indent=2))
    
    elif command == "brief":
        print(format_brief())
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
