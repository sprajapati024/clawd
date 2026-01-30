#!/usr/bin/env python3
"""
Portfolio Management System for Day Trading Bot
Manages holdings, cash, trades, and performance tracking.
"""

import csv
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class Portfolio:
    def __init__(self, data_dir: str = "/root/clawd/projects/day-trader"):
        self.data_dir = data_dir
        self.portfolio_file = os.path.join(data_dir, "portfolio.csv")
        self.trades_file = os.path.join(data_dir, "trades.csv")
        self.cash_file = os.path.join(data_dir, "cash.json")
        
        # Initialize files if they don't exist
        self._init_files()
        
        # Load current state
        self.cash = self._load_cash()
        self.portfolio = self._load_portfolio()
        
    def _init_files(self):
        """Initialize data files with headers if they don't exist."""
        # Portfolio CSV
        if not os.path.exists(self.portfolio_file):
            with open(self.portfolio_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['symbol', 'shares', 'avg_price', 'current_price', 'market_value', 'pnl'])
        
        # Trades CSV
        if not os.path.exists(self.trades_file):
            with open(self.trades_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'symbol', 'action', 'shares', 'price', 'reasoning'])
        
        # Cash JSON
        if not os.path.exists(self.cash_file):
            self._save_cash(10000.00)  # Start with $10,000 CAD
    
    def _load_cash(self) -> float:
        """Load cash balance from JSON file."""
        try:
            with open(self.cash_file, 'r') as f:
                data = json.load(f)
                return float(data.get('cash', 10000.00))
        except (FileNotFoundError, json.JSONDecodeError):
            return 10000.00
    
    def _save_cash(self, cash: float):
        """Save cash balance to JSON file."""
        with open(self.cash_file, 'w') as f:
            json.dump({'cash': cash, 'last_updated': datetime.now().isoformat()}, f)
    
    def _load_portfolio(self) -> Dict[str, Dict]:
        """Load portfolio from CSV file."""
        portfolio = {}
        try:
            with open(self.portfolio_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    portfolio[row['symbol']] = {
                        'shares': float(row['shares']),
                        'avg_price': float(row['avg_price']),
                        'current_price': float(row['current_price']),
                        'market_value': float(row['market_value']),
                        'pnl': float(row['pnl'])
                    }
        except (FileNotFoundError, KeyError):
            pass
        return portfolio
    
    def _save_portfolio(self):
        """Save portfolio to CSV file."""
        with open(self.portfolio_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['symbol', 'shares', 'avg_price', 'current_price', 'market_value', 'pnl'])
            
            for symbol, data in self.portfolio.items():
                writer.writerow([
                    symbol,
                    data['shares'],
                    data['avg_price'],
                    data['current_price'],
                    data['market_value'],
                    data['pnl']
                ])
    
    def _log_trade(self, timestamp: str, symbol: str, action: str, shares: float, price: float, reasoning: str):
        """Log a trade to the trades CSV file."""
        with open(self.trades_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, symbol, action, shares, price, reasoning])
    
    def buy(self, symbol: str, shares: int, price: float, reasoning: str = "") -> bool:
        """
        Buy shares of a stock.
        
        Args:
            symbol: Stock symbol
            shares: Number of shares to buy
            price: Price per share
            reasoning: Reason for the trade
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Calculate total cost
        total_cost = shares * price
        
        # Check if we have enough cash
        if total_cost > self.cash:
            print(f"❌ Insufficient cash. Need ${total_cost:.2f}, have ${self.cash:.2f}")
            return False
        
        # Check position size limit (max 10% of initial capital)
        if total_cost > 10000.00 * 0.10:  # 10% of $10,000 initial capital
            print(f"❌ Position size exceeds 10% limit. Cost: ${total_cost:.2f}, Limit: ${10000.00 * 0.10:.2f}")
            return False
        
        # Update portfolio
        if symbol in self.portfolio:
            # Existing position - update average price
            current = self.portfolio[symbol]
            total_shares = current['shares'] + shares
            total_cost_basis = (current['shares'] * current['avg_price']) + total_cost
            new_avg_price = total_cost_basis / total_shares
            
            self.portfolio[symbol] = {
                'shares': total_shares,
                'avg_price': new_avg_price,
                'current_price': price,
                'market_value': total_shares * price,
                'pnl': (price - new_avg_price) * total_shares
            }
        else:
            # New position
            self.portfolio[symbol] = {
                'shares': shares,
                'avg_price': price,
                'current_price': price,
                'market_value': shares * price,
                'pnl': 0.0
            }
        
        # Update cash
        self.cash -= total_cost
        self._save_cash(self.cash)
        
        # Log trade
        timestamp = datetime.now().isoformat()
        self._log_trade(timestamp, symbol, "BUY", shares, price, reasoning)
        
        # Save portfolio
        self._save_portfolio()
        
        print(f"✅ Bought {shares} shares of {symbol} at ${price:.2f} each (Total: ${total_cost:.2f})")
        print(f"   Reasoning: {reasoning}")
        return True
    
    def sell(self, symbol: str, shares: int, price: float, reasoning: str = "") -> bool:
        """
        Sell shares of a stock.
        
        Args:
            symbol: Stock symbol
            shares: Number of shares to sell
            price: Price per share
            reasoning: Reason for the trade
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if we have the position
        if symbol not in self.portfolio:
            print(f"❌ No position in {symbol}")
            return False
        
        position = self.portfolio[symbol]
        
        # Check if we have enough shares
        if shares > position['shares']:
            print(f"❌ Not enough shares. Have {position['shares']}, trying to sell {shares}")
            return False
        
        # Calculate proceeds
        proceeds = shares * price
        
        # Update portfolio
        if shares == position['shares']:
            # Selling entire position
            del self.portfolio[symbol]
        else:
            # Partial sale
            remaining_shares = position['shares'] - shares
            self.portfolio[symbol] = {
                'shares': remaining_shares,
                'avg_price': position['avg_price'],  # Average price stays the same
                'current_price': price,
                'market_value': remaining_shares * price,
                'pnl': (price - position['avg_price']) * remaining_shares
            }
        
        # Update cash
        self.cash += proceeds
        self._save_cash(self.cash)
        
        # Log trade
        timestamp = datetime.now().isoformat()
        self._log_trade(timestamp, symbol, "SELL", shares, price, reasoning)
        
        # Save portfolio
        self._save_portfolio()
        
        # Calculate realized P&L
        realized_pnl = (price - position['avg_price']) * shares
        
        print(f"✅ Sold {shares} shares of {symbol} at ${price:.2f} each (Total: ${proceeds:.2f})")
        print(f"   Realized P&L: ${realized_pnl:.2f}")
        print(f"   Reasoning: {reasoning}")
        return True
    
    def update_prices(self, price_updates: Dict[str, float]):
        """
        Update current prices for all holdings.
        
        Args:
            price_updates: Dictionary of symbol -> current_price
        """
        for symbol, price in price_updates.items():
            if symbol in self.portfolio:
                position = self.portfolio[symbol]
                position['current_price'] = price
                position['market_value'] = position['shares'] * price
                position['pnl'] = (price - position['avg_price']) * position['shares']
        
        self._save_portfolio()
    
    def get_portfolio(self) -> Dict[str, Dict]:
        """Get current portfolio holdings."""
        return self.portfolio.copy()
    
    def get_cash(self) -> float:
        """Get current cash balance."""
        return self.cash
    
    def get_portfolio_value(self) -> float:
        """Get total portfolio value (cash + investments)."""
        total_value = self.cash
        for position in self.portfolio.values():
            total_value += position['market_value']
        return total_value
    
    def get_performance(self) -> Dict:
        """
        Get portfolio performance metrics.
        
        Returns:
            Dict with performance metrics
        """
        total_invested = 0.0
        total_market_value = 0.0
        total_pnl = 0.0
        
        for position in self.portfolio.values():
            cost_basis = position['shares'] * position['avg_price']
            total_invested += cost_basis
            total_market_value += position['market_value']
            total_pnl += position['pnl']
        
        total_value = self.cash + total_market_value
        initial_capital = 10000.00
        total_return = total_value - initial_capital
        total_return_pct = (total_return / initial_capital) * 100
        
        return {
            'cash': self.cash,
            'invested': total_invested,
            'market_value': total_market_value,
            'total_value': total_value,
            'total_pnl': total_pnl,
            'total_return': total_return,
            'total_return_pct': total_return_pct,
            'initial_capital': initial_capital
        }
    
    def get_recent_trades(self, limit: int = 10) -> List[Dict]:
        """Get recent trades."""
        trades = []
        try:
            with open(self.trades_file, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                # Get last 'limit' trades
                for row in rows[-limit:]:
                    trades.append({
                        'timestamp': row['timestamp'],
                        'symbol': row['symbol'],
                        'action': row['action'],
                        'shares': float(row['shares']),
                        'price': float(row['price']),
                        'reasoning': row['reasoning']
                    })
        except (FileNotFoundError, KeyError):
            pass
        return trades

# Singleton instance for easy import
portfolio = Portfolio()

# Convenience functions
def buy(symbol: str, shares: int, price: float, reasoning: str = "") -> bool:
    """Convenience function to buy shares."""
    return portfolio.buy(symbol, shares, price, reasoning)

def sell(symbol: str, shares: int, price: float, reasoning: str = "") -> bool:
    """Convenience function to sell shares."""
    return portfolio.sell(symbol, shares, price, reasoning)

def get_portfolio() -> Dict[str, Dict]:
    """Convenience function to get portfolio."""
    return portfolio.get_portfolio()

def get_performance() -> Dict:
    """Convenience function to get performance."""
    return portfolio.get_performance()

def update_prices(price_updates: Dict[str, float]):
    """Convenience function to update prices."""
    portfolio.update_prices(price_updates)

def get_recent_trades(limit: int = 10) -> List[Dict]:
    """Convenience function to get recent trades."""
    return portfolio.get_recent_trades(limit)

if __name__ == "__main__":
    # Test the portfolio system
    print("🧪 Testing Portfolio System...")
    print(f"Initial cash: ${portfolio.get_cash():.2f}")
    
    # Test buy
    portfolio.buy("AAPL", 10, 150.00, "Technical breakout")
    portfolio.buy("MSFT", 5, 300.00, "Strong earnings")
    
    # Test sell
    portfolio.sell("AAPL", 5, 155.00, "Taking profits")
    
    # Update prices
    portfolio.update_prices({"AAPL": 156.00, "MSFT": 305.00})
    
    # Get performance
    perf = portfolio.get_performance()
    print(f"\n📊 Performance:")
    print(f"  Cash: ${perf['cash']:.2f}")
    print(f"  Portfolio Value: ${perf['total_value']:.2f}")
    print(f"  Total P&L: ${perf['total_pnl']:.2f}")
    print(f"  Total Return: ${perf['total_return']:.2f} ({perf['total_return_pct']:.2f}%)")
    
    # Show portfolio
    print(f"\n📈 Portfolio Holdings:")
    for symbol, position in portfolio.get_portfolio().items():
        print(f"  {symbol}: {position['shares']} shares @ ${position['avg_price']:.2f} avg")
        print(f"     Current: ${position['current_price']:.2f}, Value: ${position['market_value']:.2f}")
        print(f"     P&L: ${position['pnl']:.2f}")