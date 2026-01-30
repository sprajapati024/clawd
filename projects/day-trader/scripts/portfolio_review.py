#!/usr/bin/env python3
"""
Portfolio Review Command
Generates clean Telegram-friendly portfolio summaries.
"""

import os
import sys
import csv
from datetime import datetime
from typing import Dict, List

# Add parent directory to path for portfolio import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from portfolio import Portfolio

class PortfolioReview:
    def __init__(self):
        self.portfolio = Portfolio()
    
    def generate_summary(self, include_trades: bool = True, trade_limit: int = 5) -> str:
        """
        Generate Telegram-friendly portfolio summary.
        
        Args:
            include_trades: Whether to include recent trades
            trade_limit: Number of recent trades to include
            
        Returns:
            Formatted summary string
        """
        lines = []
        
        # Header
        lines.append("📊 PORTFOLIO REVIEW")
        lines.append(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}")
        lines.append("")
        
        # Performance metrics
        perf = self.portfolio.get_performance()
        
        lines.append("💰 PERFORMANCE")
        lines.append(f"• Cash: ${perf['cash']:.2f}")
        lines.append(f"• Invested: ${perf['invested']:.2f}")
        lines.append(f"• Market Value: ${perf['market_value']:.2f}")
        lines.append(f"• Total Value: ${perf['total_value']:.2f}")
        lines.append("")
        
        # P&L section
        total_pnl = perf['total_pnl']
        total_return = perf['total_return']
        total_return_pct = perf['total_return_pct']
        
        # Color code P&L
        if total_pnl >= 0:
            pnl_emoji = "📈"
            pnl_prefix = "+"
        else:
            pnl_emoji = "📉"
            pnl_prefix = ""
        
        lines.append(f"{pnl_emoji} PROFIT & LOSS")
        lines.append(f"• Unrealized P&L: {pnl_prefix}${total_pnl:.2f}")
        lines.append(f"• Total Return: {pnl_prefix}${total_return:.2f} ({pnl_prefix}{total_return_pct:.2f}%)")
        lines.append(f"• vs Initial: ${perf['initial_capital']:.2f} → ${perf['total_value']:.2f}")
        lines.append("")
        
        # Holdings summary
        holdings = self.portfolio.get_portfolio()
        if holdings:
            lines.append("📦 CURRENT HOLDINGS")
            
            # Sort by market value (descending)
            sorted_holdings = sorted(
                holdings.items(),
                key=lambda x: x[1]['market_value'],
                reverse=True
            )
            
            for symbol, position in sorted_holdings:
                shares = position['shares']
                avg_price = position['avg_price']
                current_price = position['current_price']
                market_value = position['market_value']
                pnl = position['pnl']
                pnl_pct = (pnl / (shares * avg_price)) * 100 if shares * avg_price > 0 else 0
                
                # Emoji based on performance
                if pnl >= 0:
                    holding_emoji = "✅"
                    pnl_prefix = "+"
                else:
                    holding_emoji = "⚠️"
                    pnl_prefix = ""
                
                lines.append(f"{holding_emoji} {symbol}")
                lines.append(f"  Shares: {shares}")
                lines.append(f"  Avg Cost: ${avg_price:.2f}")
                lines.append(f"  Current: ${current_price:.2f}")
                lines.append(f"  Value: ${market_value:.2f}")
                lines.append(f"  P&L: {pnl_prefix}${pnl:.2f} ({pnl_prefix}{pnl_pct:.2f}%)")
        else:
            lines.append("📭 NO CURRENT HOLDINGS")
            lines.append("Portfolio is 100% cash")
        
        lines.append("")
        
        # Recent trades
        if include_trades:
            trades = self.portfolio.get_recent_trades(trade_limit)
            if trades:
                lines.append("🔄 RECENT TRADES")
                
                for trade in trades:
                    timestamp = datetime.fromisoformat(trade['timestamp'].replace('Z', '+00:00'))
                    est_time = timestamp.strftime('%m/%d %H:%M')
                    
                    action = trade['action']
                    symbol = trade['symbol']
                    shares = trade['shares']
                    price = trade['price']
                    
                    # Action emoji
                    if action == "BUY":
                        action_emoji = "🟢"
                    else:
                        action_emoji = "🔴"
                    
                    lines.append(f"{action_emoji} {est_time}: {action} {shares} {symbol} @ ${price:.2f}")
                    
                    # Add reasoning if available (truncated)
                    reasoning = trade.get('reasoning', '')
                    if reasoning and len(reasoning) > 0:
                        short_reason = reasoning[:60] + "..." if len(reasoning) > 60 else reasoning
                        lines.append(f"   📝 {short_reason}")
        
        # Risk metrics
        lines.append("")
        lines.append("⚠️ RISK METRICS")
        
        total_value = perf['total_value']
        cash_pct = (perf['cash'] / total_value) * 100 if total_value > 0 else 100
        invested_pct = 100 - cash_pct
        
        lines.append(f"• Cash Allocation: {cash_pct:.1f}%")
        lines.append(f"• Invested Allocation: {invested_pct:.1f}%")
        
        # Position concentration
        if holdings:
            largest_position = max(holdings.values(), key=lambda x: x['market_value'])
            largest_pct = (largest_position['market_value'] / total_value) * 100
            lines.append(f"• Largest Position: {largest_pct:.1f}% of portfolio")
        
        lines.append(f"• Max Position Limit: 10%")
        lines.append(f"• Stop Loss: 5%")
        lines.append(f"• Take Profit: 10%")
        
        # Footer
        lines.append("")
        lines.append("🤖 Automated Trading Bot")
        lines.append("📅 Next analysis: 4:30 PM EST daily")
        
        return "\n".join(lines)
    
    def compare_to_sp500(self) -> str:
        """
        Compare portfolio performance to S&P 500 benchmark.
        Note: This is a mock implementation - in production, use real data.
        
        Returns:
            Comparison string
        """
        # Mock S&P 500 performance (would use real API in production)
        # Assuming S&P 500 returned ~8% annually
        import random
        from datetime import datetime
        
        # Generate mock benchmark data
        days_since_start = 30  # Assuming 30 days of operation
        daily_return = 0.00032  # ~8% annualized daily return
        sp500_start = 10000.00
        sp500_current = sp500_start * ((1 + daily_return) ** days_since_start)
        sp500_return = sp500_current - sp500_start
        sp500_return_pct = (sp500_return / sp500_start) * 100
        
        # Portfolio performance
        perf = self.portfolio.get_performance()
        portfolio_return_pct = perf['total_return_pct']
        
        # Comparison
        outperformance = portfolio_return_pct - sp500_return_pct
        
        lines = []
        lines.append("📈 VS S&P 500 BENCHMARK")
        lines.append("")
        lines.append(f"Your Portfolio: {portfolio_return_pct:+.2f}%")
        lines.append(f"S&P 500 (mock): {sp500_return_pct:+.2f}%")
        lines.append("")
        
        if outperformance > 0:
            lines.append(f"✅ Outperforming by {outperformance:.2f}%")
        elif outperformance < 0:
            lines.append(f"⚠️ Underperforming by {abs(outperformance):.2f}%")
        else:
            lines.append("📊 Matching benchmark")
        
        return "\n".join(lines)

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate portfolio review")
    parser.add_argument("--no-trades", action="store_true", help="Exclude recent trades")
    parser.add_argument("--trades", type=int, default=5, help="Number of recent trades to show")
    parser.add_argument("--benchmark", action="store_true", help="Include S&P 500 comparison")
    parser.add_argument("--simple", action="store_true", help="Simple output (no emojis)")
    
    args = parser.parse_args()
    
    review = PortfolioReview()
    
    # Generate summary
    summary = review.generate_summary(
        include_trades=not args.no_trades,
        trade_limit=args.trades
    )
    
    # Remove emojis if simple mode
    if args.simple:
        import re
        # Remove common emojis and symbols
        summary = re.sub(r'[📊📈📉💰📦🔄⚠️✅🟢🔴📝🤖📅]+', '', summary)
        summary = re.sub(r'•', '-', summary)
    
    print(summary)
    
    # Add benchmark if requested
    if args.benchmark:
        print("\n" + review.compare_to_sp500())

if __name__ == "__main__":
    main()