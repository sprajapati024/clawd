#!/usr/bin/env python3
"""
Telegram Reporter for Trading Bot
Sends formatted reports to Telegram with guaranteed delivery tracking.
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional

class TelegramReporter:
    """Send trading reports to Telegram with guaranteed output."""
    
    def __init__(self, bot_token: str = None, chat_id: str = None):
        """
        Initialize Telegram reporter.
        
        Args:
            bot_token: Telegram bot token (from @BotFather)
            chat_id: Telegram chat ID to send messages to
        """
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID", "")
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        # Delivery tracking
        self.delivery_log = "/tmp/telegram_delivery.log"
        
    def is_configured(self) -> bool:
        """Check if Telegram is configured."""
        return bool(self.bot_token and self.chat_id)
    
    def format_portfolio_report(self, portfolio_data: Dict[str, Any]) -> str:
        """
        Format portfolio data for Telegram.
        
        Args:
            portfolio_data: Portfolio performance data
            
        Returns:
            Formatted Telegram message
        """
        cash = portfolio_data.get('cash', 0)
        total_value = portfolio_data.get('total_value', 0)
        total_pnl = portfolio_data.get('total_pnl', 0)
        total_return_pct = portfolio_data.get('total_return_pct', 0)
        
        # Determine emoji based on performance
        if total_pnl > 0:
            trend_emoji = "📈"
        elif total_pnl < 0:
            trend_emoji = "📉"
        else:
            trend_emoji = "📊"
        
        message = [
            f"{trend_emoji} *PORTFOLIO UPDATE*",
            f"*Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}",
            "",
            f"💰 *Cash:* `${cash:.2f}`",
            f"🏦 *Total Value:* `${total_value:.2f}`",
            f"📊 *P&L:* `${total_pnl:+.2f}`",
            f"📈 *Return:* `{total_return_pct:+.2f}%`",
            ""
        ]
        
        # Add holdings if available
        holdings = portfolio_data.get('holdings', {})
        if holdings:
            message.append("*📦 HOLDINGS:*")
            for symbol, data in holdings.items():
                pnl = data.get('pnl', 0)
                pnl_pct = ((data.get('current_price', 0) - data.get('avg_price', 0)) / data.get('avg_price', 0) * 100) if data.get('avg_price', 0) > 0 else 0
                pnl_emoji = "🟢" if pnl > 0 else "🔴" if pnl < 0 else "⚪"
                message.append(f"{pnl_emoji} *{symbol}:* {data.get('shares', 0):.0f} shares")
                message.append(f"  `${data.get('market_value', 0):.2f}` | `{pnl_pct:+.2f}%`")
        
        return "\n".join(message)
    
    def format_trade_report(self, trade_data: Dict[str, Any]) -> str:
        """
        Format trade execution results for Telegram.
        
        Args:
            trade_data: Trade execution results
            
        Returns:
            Formatted Telegram message
        """
        executed = trade_data.get('executed_trades', [])
        skipped = trade_data.get('skipped_trades', [])
        errors = trade_data.get('errors', [])
        
        message = [
            "🔄 *TRADE EXECUTION REPORT*",
            f"*Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}",
            ""
        ]
        
        if executed:
            message.append(f"✅ *Executed {len(executed)} trades:*")
            for trade in executed:
                action_emoji = "🟢" if trade.get('action') == "BUY" else "🔴"
                message.append(f"{action_emoji} *{trade.get('action')}* {trade.get('shares')} {trade.get('symbol')}")
                message.append(f"  `@ ${trade.get('price', 0):.2f}` | `${trade.get('shares', 0) * trade.get('price', 0):.2f}`")
                if trade.get('reasoning'):
                    message.append(f"  _Reason: {trade.get('reasoning')}_")
                message.append("")
        else:
            message.append("📭 *No trades executed*")
            # Include no_trade_reason if available
            summary = trade_data.get('summary', {})
            no_trade_reason = summary.get('no_trade_reason')
            if no_trade_reason:
                message.append(f"  _Reason: {no_trade_reason}_")
            message.append("")
        
        if skipped:
            message.append(f"⚠️ *Skipped {len(skipped)} trades:*")
            for skip in skipped[:3]:  # Limit to 3
                message.append(f"  • {skip.get('symbol', 'Unknown')}: {skip.get('reason', 'No reason')}")
            if len(skipped) > 3:
                message.append(f"  ... and {len(skipped) - 3} more")
            message.append("")
        
        if errors:
            message.append(f"❌ *Errors ({len(errors)}):*")
            for error in errors[:2]:  # Limit to 2
                message.append(f"  • {error.get('symbol', 'System')}: {error.get('error', 'Unknown error')}")
            if len(errors) > 2:
                message.append(f"  ... and {len(errors) - 2} more")
        
        return "\n".join(message)
    
    def format_market_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """
        Format market analysis for Telegram.
        
        Args:
            analysis_data: Market analysis data
            
        Returns:
            Formatted Telegram message
        """
        condition = analysis_data.get('market_condition', 'unknown').upper()
        summary = analysis_data.get('market_summary', 'No summary available')
        
        # Condition emojis
        condition_emojis = {
            'BULLISH': '🚀',
            'BEARISH': '🐻',
            'NEUTRAL': '⚖️',
            'VOLATILE': '🌊'
        }
        condition_emoji = condition_emojis.get(condition, '📊')
        
        message = [
            f"{condition_emoji} *MARKET ANALYSIS*",
            f"*Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}",
            "",
            f"*Condition:* {condition} {condition_emoji}",
            f"*Summary:* {summary}",
            ""
        ]
        
        # Add recommendations if available
        recommendations = analysis_data.get('trade_recommendations', [])
        if recommendations:
            message.append(f"🎯 *{len(recommendations)} RECOMMENDATIONS:*")
            for rec in recommendations[:3]:  # Limit to 3
                action = rec.get('action', 'HOLD')
                action_emoji = "🟢" if action == "BUY" else "🔴" if action == "SELL" else "⚪"
                message.append(f"{action_emoji} *{action}* {rec.get('symbol')}")
                if rec.get('shares'):
                    message.append(f"  `{rec.get('shares')} shares` | `max ${rec.get('max_price', 0):.2f}`")
                if rec.get('reasoning'):
                    message.append(f"  _Reason: {rec.get('reasoning')}_")
                message.append("")
        
        return "\n".join(message)
    
    def format_daily_summary(self, 
                           portfolio_data: Dict[str, Any],
                           trade_data: Dict[str, Any],
                           analysis_data: Dict[str, Any]) -> str:
        """
        Format complete daily summary for Telegram.
        
        Args:
            portfolio_data: Portfolio performance
            trade_data: Trade execution results
            analysis_data: Market analysis
            
        Returns:
            Complete daily summary message
        """
        message = [
            "📊 *DAILY TRADING SUMMARY*",
            f"*Date:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}",
            "=" * 30,
            ""
        ]
        
        # Portfolio section
        portfolio_msg = self.format_portfolio_report(portfolio_data)
        message.append(portfolio_msg.split('\n', 1)[1])  # Skip first line (already have header)
        message.append("")
        
        # Trade section
        trade_msg = self.format_trade_report(trade_data)
        message.append(trade_msg)
        message.append("")
        
        # Market analysis section
        analysis_msg = self.format_market_analysis(analysis_data)
        message.append(analysis_msg)
        message.append("")
        
        # Footer
        message.append("=" * 30)
        message.append("🤖 *Trading Bot Status:* `OPERATIONAL`")
        message.append(f"📝 *Next Update:* `Tomorrow 4:30 PM EST`")
        
        return "\n".join(message)
    
    def send_message(self, text: str, parse_mode: str = "Markdown") -> Dict[str, Any]:
        """
        Send message to Telegram.
        
        Args:
            text: Message text
            parse_mode: Parse mode (Markdown or HTML)
            
        Returns:
            API response or error information
        """
        if not self.is_configured():
            return {
                "success": False,
                "error": "Telegram not configured",
                "message": "Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables"
            }
        
        try:
            # Truncate if too long (Telegram limit is 4096 chars)
            if len(text) > 4000:
                text = text[:4000] + "\n\n...[Message truncated]"
            
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": parse_mode,
                    "disable_web_page_preview": True
                },
                timeout=10
            )
            
            result = response.json()
            
            # Log delivery
            self._log_delivery(text[:100], result.get('ok', False))
            
            if result.get('ok'):
                return {
                    "success": True,
                    "message_id": result.get('result', {}).get('message_id'),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": result.get('description', 'Unknown error'),
                    "code": result.get('error_code', 0)
                }
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            self._log_delivery(text[:100], False, error_msg)
            return {
                "success": False,
                "error": error_msg
            }
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self._log_delivery(text[:100], False, error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    def _log_delivery(self, message_preview: str, success: bool, error: str = None):
        """Log message delivery attempt."""
        try:
            with open(self.delivery_log, 'a') as f:
                log_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "message_preview": message_preview,
                    "success": success,
                    "error": error
                }
                f.write(json.dumps(log_entry) + '\n')
        except:
            pass  # Don't fail if logging fails
    
    def get_delivery_stats(self) -> Dict[str, Any]:
        """Get delivery statistics from log."""
        try:
            if not os.path.exists(self.delivery_log):
                return {"total": 0, "success": 0, "failure": 0}
            
            with open(self.delivery_log, 'r') as f:
                lines = f.readlines()
            
            total = len(lines)
            success = 0
            failures = []
            
            for line in lines[-100:]:  # Last 100 entries
                try:
                    entry = json.loads(line.strip())
                    if entry.get('success'):
                        success += 1
                    else:
                        failures.append(entry)
                except:
                    pass
            
            return {
                "total": total,
                "success": success,
                "failure": total - success,
                "success_rate": (success / total * 100) if total > 0 else 0,
                "recent_failures": failures[-5:] if failures else []
            }
            
        except Exception as e:
            return {"error": str(e)}

def main():
    """Test the Telegram reporter."""
    print("🧪 Testing Telegram Reporter...")
    print("=" * 50)
    
    # Check configuration
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    
    if not bot_token or not chat_id:
        print("⚠️ Telegram not configured. Testing with mock data only.")
        print("   Set environment variables:")
        print("   - TELEGRAM_BOT_TOKEN")
        print("   - TELEGRAM_CHAT_ID")
        print("")
    
    reporter = TelegramReporter()
    
    # Generate test data
    print("1. Generating test data...")
    from mock_data import MockDataGenerator
    generator = MockDataGenerator(seed=42)
    
    portfolio_data = generator.generate_portfolio_state()
    trade_data = {
        "executed_trades": generator.generate_trades(2),
        "skipped_trades": [
            {"symbol": "AAPL", "reason": "Risk limit exceeded"},
            {"symbol": "TSLA", "reason": "Insufficient cash"}
        ],
        "errors": []
    }
    analysis_data = generator.generate_market_analysis()
    
    print("2. Formatting reports...")
    
    # Test portfolio report
    portfolio_msg = reporter.format_portfolio_report(portfolio_data)
    print(f"\n📊 Portfolio Report ({len(portfolio_msg)} chars):")
    print("-" * 40)
    print(portfolio_msg[:200] + "..." if len(portfolio_msg) > 200 else portfolio_msg)
    
    # Test trade report
    trade_msg = reporter.format_trade_report(trade_data)
    print(f"\n🔄 Trade Report ({len(trade_msg)} chars):")
    print("-" * 40)
    print(trade_msg[:200] + "..." if len(trade_msg) > 200 else trade_msg)
    
    # Test market analysis
    analysis_msg = reporter.format_market_analysis(analysis_data)
    print(f"\n📈 Market Analysis ({len(analysis_msg)} chars):")
    print("-" * 40)
    print(analysis_msg[:200] + "..." if len(analysis_msg) > 200 else analysis_msg)
    
    # Test daily summary
    daily_msg = reporter.format_daily_summary(portfolio_data, trade_data, analysis_data)
    print(f"\n📋 Daily Summary ({len(daily_msg)} chars):")
    print("-" * 40)
    print(daily_msg[:300] + "..." if len(daily_msg) > 300 else daily_msg)
    
    # Test sending (if configured)
    if reporter.is_configured():
        print(f"\n3. Testing Telegram send (if configured)...")
        result = reporter.send_message("🤖 Trading Bot Test Message\nTime: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S EST"))
        
        if result.get('success'):
            print(f"   ✅ Message sent successfully (ID: {result.get('message_id')})")
        else:
            print(f"   ❌ Failed to send: {result.get('error')}")
    else:
        print(f"\n3. Telegram not configured - skipping send test")
        print("   To test sending, set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")
    
    # Show delivery stats
    stats = reporter.get_delivery_stats()
    print(f"\n4. Delivery Statistics:")
    print(f"   • Total attempts: {stats.get('total', 0)}")
    print(f"   • Success rate: {stats.get('success_rate', 0):.1f}%")
    
    print("\n✅ Telegram reporter test completed!")

if __name__ == "__main__":
    main()