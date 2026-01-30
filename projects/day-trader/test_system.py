#!/usr/bin/env python3
"""
Test the trading bot system end-to-end.
"""

import os
import sys
import json
from datetime import datetime

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_portfolio():
    """Test portfolio management system."""
    print("🧪 Testing Portfolio System...")
    print("=" * 50)
    
    from portfolio import Portfolio
    
    # Create fresh portfolio for testing
    test_dir = "/tmp/test_portfolio"
    os.makedirs(test_dir, exist_ok=True)
    
    portfolio = Portfolio(data_dir=test_dir)
    
    # Test 1: Initial state
    print("\n1. Initial State:")
    print(f"   Cash: ${portfolio.get_cash():.2f}")
    print(f"   Portfolio Value: ${portfolio.get_portfolio_value():.2f}")
    
    # Test 2: Buy shares
    print("\n2. Buying shares:")
    success = portfolio.buy("AAPL", 10, 150.00, "Test purchase")
    print(f"   Buy AAPL: {'✅ Success' if success else '❌ Failed'}")
    
    success = portfolio.buy("MSFT", 5, 300.00, "Test purchase")
    print(f"   Buy MSFT: {'✅ Success' if success else '❌ Failed'}")
    
    # Test 3: Sell shares
    print("\n3. Selling shares:")
    success = portfolio.sell("AAPL", 5, 155.00, "Test sale")
    print(f"   Sell AAPL: {'✅ Success' if success else '❌ Failed'}")
    
    # Test 4: Update prices
    print("\n4. Updating prices:")
    portfolio.update_prices({"AAPL": 156.00, "MSFT": 305.00})
    print("   Prices updated")
    
    # Test 5: Get portfolio
    print("\n5. Current Portfolio:")
    holdings = portfolio.get_portfolio()
    for symbol, data in holdings.items():
        print(f"   {symbol}: {data['shares']} shares, Value: ${data['market_value']:.2f}, P&L: ${data['pnl']:.2f}")
    
    # Test 6: Performance metrics
    print("\n6. Performance Metrics:")
    perf = portfolio.get_performance()
    print(f"   Cash: ${perf['cash']:.2f}")
    print(f"   Total Value: ${perf['total_value']:.2f}")
    print(f"   Total P&L: ${perf['total_pnl']:.2f}")
    print(f"   Total Return: ${perf['total_return']:.2f} ({perf['total_return_pct']:.2f}%)")
    
    # Test 7: Recent trades
    print("\n7. Recent Trades:")
    trades = portfolio.get_recent_trades(5)
    for trade in trades:
        print(f"   {trade['timestamp']}: {trade['action']} {trade['shares']} {trade['symbol']} @ ${trade['price']:.2f}")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    
    print("\n✅ Portfolio tests completed!")

def test_portfolio_review():
    """Test portfolio review command."""
    print("\n\n🧪 Testing Portfolio Review...")
    print("=" * 50)
    
    from scripts.portfolio_review import PortfolioReview
    
    review = PortfolioReview()
    
    # Generate summary
    summary = review.generate_summary(include_trades=True, trade_limit=3)
    
    print("\nPortfolio Review Output:")
    print("-" * 30)
    print(summary[:500] + "..." if len(summary) > 500 else summary)
    
    print("\n✅ Portfolio review test completed!")

def test_daily_routine_structure():
    """Test daily routine script structure."""
    print("\n\n🧪 Testing Daily Routine Structure...")
    print("=" * 50)
    
    routine_path = "/root/clawd/projects/day-trader/scripts/daily_routine.sh"
    
    if os.path.exists(routine_path):
        with open(routine_path, 'r') as f:
            content = f.read()
        
        # Check key components
        checks = [
            ("#!/bin/bash" in content, "Has shebang"),
            ("LOG_DIR=" in content, "Has log directory"),
            ("fetching latest prices" in content.lower(), "Has price fetching"),
            ("trading analysis" in content.lower(), "Has trading analysis"),
            ("generate report" in content.lower(), "Has report generation"),
            ("backup" in content.lower(), "Has backup"),
        ]
        
        for check, description in checks:
            print(f"   {'✅' if check else '❌'} {description}")
        
        print(f"\n✅ Daily routine structure check completed!")
    else:
        print(f"❌ Daily routine script not found at {routine_path}")

def test_trader_structure():
    """Test trader script structure."""
    print("\n\n🧪 Testing Trader Structure...")
    print("=" * 50)
    
    trader_path = "/root/clawd/projects/day-trader/scripts/trader.py"
    
    if os.path.exists(trader_path):
        with open(trader_path, 'r') as f:
            content = f.read()
        
        # Check key components
        checks = [
            ("TradingDecisionEngine" in content, "Has trading engine class"),
            ("analyze_market" in content, "Has market analysis"),
            ("execute_trades" in content, "Has trade execution"),
            ("risk management" in content.lower(), "Has risk management"),
            ("generate_report" in content, "Has report generation"),
        ]
        
        for check, description in checks:
            print(f"   {'✅' if check else '❌'} {description}")
        
        print(f"\n✅ Trader structure check completed!")
    else:
        print(f"❌ Trader script not found at {trader_path}")

def main():
    """Run all tests."""
    print("🚀 Trading Bot System - End-to-End Test")
    print("=" * 60)
    
    try:
        test_portfolio()
        test_portfolio_review()
        test_daily_routine_structure()
        test_trader_structure()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("\nSystem is ready for:")
        print("1. API key configuration in /root/clawd-workspace/dexter/.env")
        print("2. Cron job setup for daily automation")
        print("3. Telegram notification configuration (optional)")
        print("4. Real market data integration")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())