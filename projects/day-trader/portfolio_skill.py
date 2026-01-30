#!/usr/bin/env python3
"""
Clawdbot Skill: Portfolio Command
Provides /portfolio command for Telegram integration.
"""

import os
import sys
from typing import Dict, Any

# Add project directory to path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from scripts.portfolio_review import PortfolioReview

def portfolio_command(args: Dict[str, Any] = None) -> str:
    """
    Handle /portfolio command.
    
    Args:
        args: Command arguments (optional)
        
    Returns:
        Formatted portfolio summary
    """
    try:
        review = PortfolioReview()
        
        # Parse arguments
        include_benchmark = False
        simple_mode = False
        
        if args:
            if args.get("benchmark"):
                include_benchmark = True
            if args.get("simple"):
                simple_mode = True
        
        # Generate summary
        summary = review.generate_summary(include_trades=True, trade_limit=5)
        
        # Apply simple mode if requested
        if simple_mode:
            import re
            summary = re.sub(r'[📊📈📉💰📦🔄⚠️✅🟢🔴📝🤖📅]+', '', summary)
            summary = re.sub(r'•', '-', summary)
        
        # Add benchmark if requested
        if include_benchmark:
            benchmark = review.compare_to_sp500()
            summary = f"{summary}\n\n{benchmark}"
        
        return summary
        
    except Exception as e:
        return f"❌ Error generating portfolio report: {str(e)}"

def help_command() -> str:
    """Return help text for the portfolio command."""
    return """📊 /portfolio - View your trading portfolio

Options:
  /portfolio - Basic portfolio summary
  /portfolio benchmark - Include S&P 500 comparison
  /portfolio simple - Simple text (no emojis)

Examples:
  /portfolio
  /portfolio benchmark
  /portfolio simple"""

# Test the command
if __name__ == "__main__":
    print("🧪 Testing Portfolio Skill...")
    print("=" * 50)
    
    # Test basic command
    result = portfolio_command()
    print("Basic portfolio command output (first 200 chars):")
    print(result[:200] + "..." if len(result) > 200 else result)
    print("\n" + "=" * 50)
    
    # Test with benchmark
    result = portfolio_command({"benchmark": True})
    print("\nWith benchmark (first 200 chars):")
    print(result[:200] + "..." if len(result) > 200 else result)
    print("\n" + "=" * 50)
    
    # Test help
    print("\nHelp command:")
    print(help_command())