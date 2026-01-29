#!/usr/bin/env python3
"""
Mistral Email Preprocessor
Analyzes emails locally, sends only summaries to Claude
"""

import subprocess
import json
import sys
from datetime import datetime

def call_mistral(prompt):
    """Call local Mistral via Ollama"""
    result = subprocess.run(
        ['ollama', 'run', 'mistral:7b', prompt],
        capture_output=True,
        text=True,
        timeout=90
    )
    return result.stdout.strip()

def preprocess_email(email_text, sender, subject):
    """Preprocess a single email with Mistral"""
    
    prompt = f"""Analyze this email and provide a brief summary in this exact format:
Category: [promotional/personal/work/automated/spam]
Priority: [high/medium/low]
Action needed: [yes/no]
Summary: [1-2 sentences max]

Email from: {sender}
Subject: {subject}
Body:
{email_text[:500]}
"""
    
    try:
        # Call Mistral locally
        response = call_mistral(prompt)
        
        # Log token usage (approximate)
        input_tokens = len(prompt.split())
        output_tokens = len(response.split())
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'task': 'email_preprocess',
            'engine': 'mistral_local',
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'cost': 0.00
        }
        
        # Log to tracking file
        with open('/var/log/clarke-monitor/mistral-usage.jsonl', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return {
            'success': True,
            'analysis': response,
            'tokens_used': input_tokens + output_tokens,
            'cost': 0.00
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'tokens_used': 0,
            'cost': 0.00
        }

if __name__ == '__main__':
    # Test with sample email
    test_email = """
    Hi Shirin,
    
    This is a test email to verify the Mistral preprocessing system works.
    Please confirm receipt.
    
    Thanks,
    Test
    """
    
    result = preprocess_email(test_email, "test@example.com", "Test Email")
    print(json.dumps(result, indent=2))
