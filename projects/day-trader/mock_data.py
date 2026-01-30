#!/usr/bin/env python3
"""
Mock Data Generator for Deterministic Testing
Provides consistent, predictable data for testing the trading system.
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

class MockDataGenerator:
    """Generate deterministic mock data for testing."""
    
    def __init__(self, seed: int = 42):
        """Initialize with a seed for deterministic output."""
        self.seed = seed
        random.seed(seed)
        
        # Base prices for common stocks (deterministic with seed)
        self.base_prices = {
            "AAPL": 150.00,
            "MSFT": 300.00,
            "GOOGL": 140.00,
            "AMZN": 170.00,
            "TSLA": 180.00,
            "NVDA": 120.00,
            "META": 350.00,
            "BRK.B": 400.00,
            "JPM": 150.00,
            "V": 250.00
        }
    
    def generate_prices(self, symbols: List[str] = None) -> Dict[str, float]:
        """
        Generate deterministic mock prices.
        
        Args:
            symbols: List of symbols to generate prices for
            
        Returns:
            Dictionary of symbol -> price
        """
        if symbols is None:
            symbols = list(self.base_prices.keys())
        
        prices = {}
        for symbol in symbols:
            if symbol in self.base_prices:
                base = self.base_prices[symbol]
                # Add deterministic "random" variation based on symbol hash
                variation = (hash(symbol) % 100) / 100.0 * 10  # 0-10% variation
                price = round(base + variation, 2)
                prices[symbol] = price
            else:
                # Generate price for unknown symbol
                price = 100.00 + (hash(symbol) % 100)  # 100-200 range
                prices[symbol] = round(price, 2)
        
        return prices
    
    def generate_portfolio_state(self, cash: float = 10000.00) -> Dict[str, Any]:
        """
        Generate a deterministic portfolio state for testing.
        
        Args:
            cash: Starting cash amount
            
        Returns:
            Portfolio state dictionary
        """
        # Generate some holdings
        holdings = {}
        symbols = ["AAPL", "MSFT", "NVDA"][:2]  # Always 2 holdings for testing
        
        for i, symbol in enumerate(symbols):
            shares = 5 + i  # 5, 6 shares
            avg_price = self.base_prices[symbol] * 0.95  # Bought at 5% discount
            current_price = self.base_prices[symbol] * (1 + (i * 0.02))  # Some gain
            
            holdings[symbol] = {
                'shares': float(shares),
                'avg_price': round(avg_price, 2),
                'current_price': round(current_price, 2),
                'market_value': round(shares * current_price, 2),
                'pnl': round(shares * (current_price - avg_price), 2)
            }
        
        # Calculate totals
        total_invested = sum(h['shares'] * h['avg_price'] for h in holdings.values())
        total_market_value = sum(h['market_value'] for h in holdings.values())
        total_pnl = sum(h['pnl'] for h in holdings.values())
        total_value = cash + total_market_value
        
        return {
            'cash': cash,
            'holdings': holdings,
            'total_invested': round(total_invested, 2),
            'total_market_value': round(total_market_value, 2),
            'total_pnl': round(total_pnl, 2),
            'total_value': round(total_value, 2),
            'initial_capital': 10000.00,
            'total_return': round(total_value - 10000.00, 2),
            'total_return_pct': round(((total_value - 10000.00) / 10000.00) * 100, 2)
        }
    
    def generate_trades(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        Generate deterministic mock trades.
        
        Args:
            count: Number of trades to generate
            
        Returns:
            List of trade dictionaries
        """
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        actions = ["BUY", "SELL"]
        reasons = [
            "Technical breakout",
            "Taking profits",
            "Risk management",
            "Portfolio rebalance",
            "AI recommendation"
        ]
        
        trades = []
        base_time = datetime.now() - timedelta(days=7)
        
        for i in range(count):
            symbol = symbols[i % len(symbols)]
            action = actions[i % len(actions)]
            shares = (i + 1) * 2  # 2, 4, 6, 8, 10 shares
            price = self.base_prices.get(symbol, 100.00) * (1 + (i * 0.01))  # Slight price increase
            reason = reasons[i % len(reasons)]
            
            trade_time = base_time + timedelta(hours=i*3)
            
            trades.append({
                'timestamp': trade_time.isoformat(),
                'symbol': symbol,
                'action': action,
                'shares': float(shares),
                'price': round(price, 2),
                'reasoning': reason
            })
        
        return trades
    
    def generate_market_analysis(self) -> Dict[str, Any]:
        """
        Generate deterministic market analysis.
        
        Returns:
            Market analysis dictionary
        """
        conditions = ["bullish", "bearish", "neutral"]
        condition = conditions[hash(str(self.seed)) % len(conditions)]
        
        summaries = [
            "Market showing strength with tech leading gains.",
            "Consolidation phase with mixed sector performance.",
            "Volatility increasing ahead of earnings season.",
            "Defensive rotation observed in market sectors."
        ]
        summary = summaries[self.seed % len(summaries)]
        
        # Generate stock analysis
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        stock_analysis = []
        
        for i, symbol in enumerate(symbols):
            signals = ["BUY", "SELL", "HOLD"]
            signal = signals[i % len(signals)]
            confidence = 5 + (i * 2)  # 5, 7, 9, etc.
            
            base_price = self.base_prices.get(symbol, 100.00)
            target_price = round(base_price * (1 + (i * 0.05)), 2)  # 0-20% target
            stop_loss = round(base_price * (1 - (i * 0.02)), 2)  # 0-8% stop loss
            
            # Calculate risk/reward ratio with safe division
            price_diff = base_price - stop_loss
            if price_diff == 0:
                risk_reward = 1.0  # Default when stop_loss equals base_price
            else:
                risk_reward = round((target_price - base_price) / price_diff, 2)
            
            stock_analysis.append({
                'symbol': symbol,
                'signal': signal,
                'confidence': confidence,
                'reasoning': f"{signal} signal based on technical indicators",
                'target_price': target_price,
                'stop_loss': stop_loss,
                'risk_reward_ratio': risk_reward
            })
        
        # Generate trade recommendations
        trade_recommendations = []
        for i in range(2):  # Always 2 recommendations
            symbol = symbols[i]
            action = "BUY" if i == 0 else "SELL"
            shares = 10 if action == "BUY" else 5
            max_price = self.base_prices.get(symbol, 100.00) * 1.01  # 1% above current
            
            trade_recommendations.append({
                'action': action,
                'symbol': symbol,
                'shares': shares,
                'max_price': round(max_price, 2),
                'reasoning': f"{action} recommendation based on market analysis"
            })
        
        return {
            'market_condition': condition,
            'market_summary': summary,
            'stock_analysis': stock_analysis,
            'trade_recommendations': trade_recommendations,
            'timestamp': datetime.now().isoformat()
        }
    
    def save_test_data(self, output_dir: str = "/tmp"):
        """
        Save all test data to files for integration testing.
        
        Args:
            output_dir: Directory to save files
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Save prices
        prices = self.generate_prices()
        with open(os.path.join(output_dir, "mock_prices.json"), 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'prices': prices
            }, f, indent=2)
        
        # Save portfolio state
        portfolio = self.generate_portfolio_state()
        with open(os.path.join(output_dir, "mock_portfolio.json"), 'w') as f:
            json.dump(portfolio, f, indent=2)
        
        # Save trades
        trades = self.generate_trades()
        with open(os.path.join(output_dir, "mock_trades.json"), 'w') as f:
            json.dump(trades, f, indent=2)
        
        # Save market analysis
        analysis = self.generate_market_analysis()
        with open(os.path.join(output_dir, "mock_analysis.json"), 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"✅ Test data saved to {output_dir}/")
        print(f"   - mock_prices.json ({len(prices)} symbols)")
        print(f"   - mock_portfolio.json (portfolio state)")
        print(f"   - mock_trades.json ({len(trades)} trades)")
        print(f"   - mock_analysis.json (market analysis)")

def main():
    """Test the mock data generator."""
    print("🧪 Mock Data Generator Test")
    print("=" * 50)
    
    generator = MockDataGenerator(seed=42)
    
    # Test price generation
    prices = generator.generate_prices(["AAPL", "MSFT", "GOOGL"])
    print("\n1. Generated Prices (deterministic):")
    for symbol, price in prices.items():
        print(f"   {symbol}: ${price:.2f}")
    
    # Test portfolio state
    portfolio = generator.generate_portfolio_state()
    print("\n2. Generated Portfolio State:")
    print(f"   Cash: ${portfolio['cash']:.2f}")
    print(f"   Total Value: ${portfolio['total_value']:.2f}")
    print(f"   Total P&L: ${portfolio['total_pnl']:.2f}")
    print(f"   Return: {portfolio['total_return_pct']:.2f}%")
    
    # Test trades
    trades = generator.generate_trades(3)
    print("\n3. Generated Trades:")
    for trade in trades:
        print(f"   {trade['timestamp']}: {trade['action']} {trade['shares']} {trade['symbol']} @ ${trade['price']:.2f}")
    
    # Test market analysis
    analysis = generator.generate_market_analysis()
    print("\n4. Generated Market Analysis:")
    print(f"   Condition: {analysis['market_condition']}")
    print(f"   Summary: {analysis['market_summary']}")
    print(f"   Recommendations: {len(analysis['trade_recommendations'])}")
    
    # Save test data
    print("\n5. Saving test data...")
    generator.save_test_data()
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()