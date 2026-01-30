#!/usr/bin/env python3
"""
Trading Decision Engine
Uses DeepSeek API for AI-powered trading decisions with risk management.
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Add parent directory to path for portfolio import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from portfolio import Portfolio

class TradingDecisionEngine:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY", "")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.portfolio = Portfolio()
        
        # Risk management parameters
        self.max_position_size_pct = 0.10  # Max 10% per position
        self.stop_loss_pct = 0.05  # 5% stop loss
        self.take_profit_pct = 0.10  # 10% take profit
        
    def analyze_market(self, symbols: List[str] = None) -> Dict:
        """
        Analyze market conditions and generate trading signals.
        
        Args:
            symbols: List of symbols to analyze (default: common stocks)
            
        Returns:
            Dict with analysis results and signals
        """
        if symbols is None:
            symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "BRK.B", "JPM", "V"]
        
        # In production, this would fetch real data
        # For now, we'll use mock data and AI analysis
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "market_condition": "neutral",  # bullish, bearish, neutral
            "signals": [],
            "recommendations": []
        }
        
        # Generate AI-powered analysis
        try:
            ai_analysis = self._get_ai_analysis(symbols)
            analysis.update(ai_analysis)
        except Exception as e:
            print(f"⚠️ AI analysis failed: {e}")
            # Fallback to basic analysis
            analysis["recommendations"] = self._generate_basic_recommendations(symbols)
        
        return analysis
    
    def _get_ai_analysis(self, symbols: List[str]) -> Dict:
        """
        Get AI analysis from DeepSeek API.
        
        Args:
            symbols: List of symbols to analyze
            
        Returns:
            Dict with AI analysis
        """
        if not self.api_key:
            raise ValueError("DeepSeek API key not configured")
        
        # Prepare prompt for AI analysis
        portfolio_value = self.portfolio.get_portfolio_value()
        cash = self.portfolio.get_cash()
        holdings = self.portfolio.get_portfolio()
        
        prompt = f"""You are an expert quantitative trading analyst. Analyze the following stocks for potential trading opportunities.

STOCKS TO ANALYZE: {', '.join(symbols)}

CURRENT PORTFOLIO:
- Total Value: ${portfolio_value:.2f}
- Cash Available: ${cash:.2f}
- Current Holdings: {json.dumps(holdings, indent=2) if holdings else "None"}

RISK PARAMETERS:
- Max position size: {self.max_position_size_pct*100}% of portfolio
- Stop loss: {self.stop_loss_pct*100}%
- Take profit: {self.take_profit_pct*100}%

ANALYSIS REQUIREMENTS:
1. For each stock, provide:
   - Technical analysis (momentum, trends, support/resistance)
   - Fundamental analysis (if available)
   - Risk assessment
   - Trading signal (BUY/SELL/HOLD)
   - Confidence level (1-10)
   - Target price
   - Stop loss price

2. Overall market assessment:
   - Market condition (bullish/bearish/neutral)
   - Key risks
   - Recommended allocation

3. Specific trade recommendations:
   - Which stocks to buy/sell
   - Position sizes
   - Entry prices
   - Reasoning

Return your analysis in JSON format with this structure:
{{
  "market_condition": "bullish/bearish/neutral",
  "market_summary": "brief summary",
  "stock_analysis": [
    {{
      "symbol": "AAPL",
      "signal": "BUY/SELL/HOLD",
      "confidence": 8,
      "reasoning": "technical/fundamental analysis",
      "target_price": 160.00,
      "stop_loss": 145.00,
      "risk_reward_ratio": 2.5
    }}
  ],
  "trade_recommendations": [
    {{
      "action": "BUY",
      "symbol": "AAPL",
      "shares": 10,
      "max_price": 155.00,
      "reasoning": "detailed reasoning"
    }}
  ]
}}

Focus on risk management and realistic position sizing."""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek/deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a quantitative trading analyst specializing in risk-managed algorithmic trading."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }
        
        response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        ai_response = result["choices"][0]["message"]["content"]
        
        # Parse JSON from response
        try:
            # Extract JSON from markdown code blocks if present
            if "```json" in ai_response:
                ai_response = ai_response.split("```json")[1].split("```")[0]
            elif "```" in ai_response:
                ai_response = ai_response.split("```")[1].split("```")[0]
            
            analysis = json.loads(ai_response)
            return analysis
        except json.JSONDecodeError:
            print(f"⚠️ Failed to parse AI response as JSON: {ai_response[:200]}...")
            return {"recommendations": []}
    
    def _generate_basic_recommendations(self, symbols: List[str]) -> List[Dict]:
        """
        Generate basic recommendations when AI is unavailable.
        
        Args:
            symbols: List of symbols
            
        Returns:
            List of basic recommendations
        """
        recommendations = []
        portfolio_value = self.portfolio.get_portfolio_value()
        
        for symbol in symbols[:3]:  # Limit to 3 symbols for basic analysis
            # Simple momentum-based strategy
            recommendations.append({
                "symbol": symbol,
                "action": "BUY",
                "shares": max(1, int((portfolio_value * 0.05) / 100)),  # 5% position
                "max_price": 100.00,  # Placeholder
                "reasoning": "Basic momentum strategy - diversify portfolio",
                "confidence": 5
            })
        
        return recommendations
    
    def execute_trades(self, recommendations: List[Dict]) -> Dict:
        """
        Execute trades based on recommendations with risk checks.
        
        Args:
            recommendations: List of trade recommendations
            
        Returns:
            Dict with execution results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "executed_trades": [],
            "skipped_trades": [],
            "errors": []
        }
        
        for rec in recommendations:
            try:
                action = rec.get("action", "").upper()
                symbol = rec.get("symbol", "")
                shares = int(rec.get("shares", 0))
                price = float(rec.get("max_price", 0))
                reasoning = rec.get("reasoning", "AI recommendation")
                
                if not symbol or shares <= 0 or price <= 0:
                    results["skipped_trades"].append({
                        "symbol": symbol,
                        "reason": "Invalid parameters"
                    })
                    continue
                
                # Apply risk management checks
                if not self._check_risk_limits(symbol, shares, price, action):
                    results["skipped_trades"].append({
                        "symbol": symbol,
                        "reason": "Risk limit exceeded"
                    })
                    continue
                
                # Execute trade
                if action == "BUY":
                    success = self.portfolio.buy(symbol, shares, price, reasoning)
                elif action == "SELL":
                    success = self.portfolio.sell(symbol, shares, price, reasoning)
                else:
                    results["skipped_trades"].append({
                        "symbol": symbol,
                        "reason": f"Unknown action: {action}"
                    })
                    continue
                
                if success:
                    results["executed_trades"].append({
                        "symbol": symbol,
                        "action": action,
                        "shares": shares,
                        "price": price,
                        "reasoning": reasoning
                    })
                else:
                    results["errors"].append({
                        "symbol": symbol,
                        "error": "Trade execution failed"
                    })
                    
            except Exception as e:
                results["errors"].append({
                    "symbol": rec.get("symbol", "unknown"),
                    "error": str(e)
                })
        
        return results
    
    def _check_risk_limits(self, symbol: str, shares: int, price: float, action: str) -> bool:
        """
        Check if trade complies with risk limits.
        
        Args:
            symbol: Stock symbol
            shares: Number of shares
            price: Price per share
            action: BUY or SELL
            
        Returns:
            bool: True if within limits
        """
        if action == "BUY":
            # Check position size limit
            trade_value = shares * price
            portfolio_value = self.portfolio.get_portfolio_value()
            
            if trade_value > portfolio_value * self.max_position_size_pct:
                print(f"❌ Trade exceeds {self.max_position_size_pct*100}% position limit")
                return False
            
            # Check if we have enough cash
            if trade_value > self.portfolio.get_cash():
                print(f"❌ Insufficient cash for trade")
                return False
        
        elif action == "SELL":
            # Check if we have the position
            portfolio = self.portfolio.get_portfolio()
            if symbol not in portfolio:
                print(f"❌ No position to sell")
                return False
            
            position = portfolio[symbol]
            if shares > position['shares']:
                print(f"❌ Not enough shares to sell")
                return False
        
        return True
    
    def generate_report(self, analysis: Dict, execution_results: Dict) -> str:
        """
        Generate trading report in Telegram-friendly format.
        
        Args:
            analysis: Market analysis
            execution_results: Trade execution results
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("📊 TRADING REPORT")
        report.append(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}")
        report.append("")
        
        # Market condition
        market_cond = analysis.get("market_condition", "unknown").upper()
        report.append(f"📈 MARKET: {market_cond}")
        if "market_summary" in analysis:
            report.append(f"Summary: {analysis['market_summary']}")
        report.append("")
        
        # Portfolio snapshot
        perf = self.portfolio.get_performance()
        report.append("💰 PORTFOLIO SNAPSHOT")
        report.append(f"Cash: ${perf['cash']:.2f}")
        report.append(f"Invested: ${perf['invested']:.2f}")
        report.append(f"Market Value: ${perf['market_value']:.2f}")
        report.append(f"Total Value: ${perf['total_value']:.2f}")
        report.append(f"Total P&L: ${perf['total_pnl']:.2f}")
        report.append(f"Return: ${perf['total_return']:.2f} ({perf['total_return_pct']:.2f}%)")
        report.append("")
        
        # Trade execution summary
        executed = execution_results.get("executed_trades", [])
        skipped = execution_results.get("skipped_trades", [])
        
        report.append("🔄 TRADE EXECUTION")
        if executed:
            report.append(f"Executed {len(executed)} trades:")
            for trade in executed:
                report.append(f"  • {trade['action']} {trade['shares']} {trade['symbol']} @ ${trade['price']:.2f}")
        else:
            report.append("No trades executed")
        
        if skipped:
            report.append(f"Skipped {len(skipped)} trades (risk limits)")
        
        # Recommendations
        recommendations = analysis.get("trade_recommendations", [])
        if recommendations:
            report.append("")
            report.append("🎯 ACTIVE RECOMMENDATIONS")
            for rec in recommendations[:5]:  # Limit to 5
                action = rec.get("action", "HOLD")
                symbol = rec.get("symbol", "Unknown")
                confidence = rec.get("confidence", 0)
                reasoning = rec.get("reasoning", "")[:100]  # Truncate
                
                report.append(f"  • {action} {symbol} (Confidence: {confidence}/10)")
                if reasoning:
                    report.append(f"    {reasoning}")
        
        return "\n".join(report)

def main():
    """Main function for testing."""
    print("🤖 Trading Decision Engine Test")
    
    # Initialize engine
    engine = TradingDecisionEngine()
    
    # Analyze market
    print("🔍 Analyzing market...")
    analysis = engine.analyze_market()
    
    # Execute trades if we have recommendations
    recommendations = analysis.get("trade_recommendations", [])
    if recommendations:
        print(f"📋 Found {len(recommendations)} recommendations")
        results = engine.execute_trades(recommendations)
        
        # Generate report
        report = engine.generate_report(analysis, results)
        print("\n" + report)
    else:
        print("📭 No trade recommendations generated")
        
        # Still generate portfolio report
        perf = engine.portfolio.get_performance()
        print(f"\n💰 Portfolio Value: ${perf['total_value']:.2f}")
        print(f"📈 Return: ${perf['total_return']:.2f} ({perf['total_return_pct']:.2f}%)")

if __name__ == "__main__":
    main()