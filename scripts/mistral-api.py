#!/usr/bin/env python3
"""
Mistral local API wrapper with automatic token tracking
Uses Ollama for local inference
"""
import json
import subprocess
import sys
from pathlib import Path

TRACKER_SCRIPT = Path(__file__).parent / "token-tracker.py"

def count_tokens(text):
    """Rough token estimation (1 token ≈ 4 characters)"""
    return len(text) // 4

def log_tokens_wrapper(source, tokens, operation=""):
    """Wrapper to call token tracker script"""
    subprocess.run(
        [str(TRACKER_SCRIPT), 'log', source, str(tokens), operation],
        capture_output=True
    )

def mistral_complete(prompt, max_tokens=500, temperature=0.7):
    """
    Call Mistral locally via Ollama
    Automatically tracks token usage
    """
    # Estimate input tokens
    input_tokens = count_tokens(prompt)
    
    try:
        # Call Ollama
        result = subprocess.run(
            ['ollama', 'run', 'mistral:7b'],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        response = result.stdout.strip()
        
        # Estimate output tokens
        output_tokens = count_tokens(response)
        total_tokens = input_tokens + output_tokens
        
        # Log token usage
        log_tokens_wrapper('mistral', total_tokens, operation="completion")
        
        return {
            "success": True,
            "response": response,
            "tokens": {
                "input": input_tokens,
                "output": output_tokens,
                "total": total_tokens
            }
        }
    
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Mistral timeout",
            "response": ""
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response": ""
        }

def mistral_summarize(text, max_length=100):
    """Summarize text using Mistral"""
    prompt = f"Summarize the following text in {max_length} words or less. Be concise and extract only key information:\n\n{text}\n\nSummary:"
    return mistral_complete(prompt, max_tokens=max_length * 2)

def mistral_categorize(text, categories):
    """Categorize text into one of the provided categories"""
    cat_list = ", ".join(categories)
    prompt = f"Categorize the following text into ONE of these categories: {cat_list}\n\nText: {text}\n\nCategory (respond with ONLY the category name):"
    return mistral_complete(prompt, max_tokens=50)

def mistral_extract_keywords(text, max_keywords=5):
    """Extract keywords from text"""
    prompt = f"Extract the {max_keywords} most important keywords from this text. Respond with ONLY a comma-separated list:\n\n{text}\n\nKeywords:"
    return mistral_complete(prompt, max_tokens=100)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  mistral-api.py summarize <text>")
        print("  mistral-api.py categorize <text> <category1,category2,...>")
        print("  mistral-api.py complete <prompt>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "summarize":
        text = " ".join(sys.argv[2:])
        result = mistral_summarize(text)
        if result["success"]:
            print(result["response"])
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
    
    elif command == "categorize":
        if len(sys.argv) < 4:
            print("Usage: mistral-api.py categorize <text> <category1,category2,...>")
            sys.exit(1)
        text = sys.argv[2]
        categories = sys.argv[3].split(",")
        result = mistral_categorize(text, categories)
        if result["success"]:
            print(result["response"])
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
    
    elif command == "complete":
        prompt = " ".join(sys.argv[2:])
        result = mistral_complete(prompt)
        if result["success"]:
            print(result["response"])
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
