import yfinance as yf
import requests
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from functools import lru_cache
import time


class ContrarianMonitor:
    def __init__(self):
        self.load_credentials()
        self.last_signal = None

    def load_credentials(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not self.bot_token or not self.chat_id:
            raise ValueError(
                "Telegram credentials not found! Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables."
            )

        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    @lru_cache(maxsize=16)
    def calculate_rsi(self, prices_tuple, period=14):
        try:
            prices = list(prices_tuple)
            if len(prices) < period + 1:
                return None

            deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
            gains = [d if d > 0 else 0 for d in deltas]
            losses = [-d if d < 0 else 0 for d in deltas]

            avg_gain = sum(gains[:period]) / period
            avg_loss = sum(losses[:period]) / period

            for i in range(period, len(gains)):
                avg_gain = (avg_gain * (period - 1) + gains[i]) / period
                avg_loss = (avg_loss * (period - 1) + losses[i]) / period

            if avg_loss == 0:
                return 100

            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception as e:
            print(f"Error calculating RSI: {e}")
            return None

    @lru_cache(maxsize=16)
    def calculate_macd(self, prices_tuple):
        try:
            prices = list(prices_tuple)
            if len(prices) < 26:
                return None, None

            def calculate_ema_series(data, period):
                multiplier = 2 / (period + 1)
                ema_values = []
                sma = sum(data[:period]) / period
                ema_values.append(sma)

                for i in range(period, len(data)):
                    ema = (data[i] - ema_values[-1]) * multiplier + ema_values[-1]
                    ema_values.append(ema)

                return ema_values

            ema_12_series = calculate_ema_series(prices, 12)
            ema_26_series = calculate_ema_series(prices, 26)

            macd_line_series = []
            for i in range(len(ema_26_series)):
                macd_value = ema_12_series[i + 14] - ema_26_series[i]
                macd_line_series.append(macd_value)

            macd_line = macd_line_series[-1]

            if len(macd_line_series) < 9:
                return macd_line, None

            signal_line_series = calculate_ema_series(macd_line_series, 9)
            signal_line = signal_line_series[-1]

            return macd_line, signal_line
        except Exception as e:
            print(f"Error calculating MACD: {e}")
            return None, None

    def calculate_enhanced_signal(
        self, ratio, vix_price, rsi, macd_crossover, above_ma200, spy_price, ma200_value
    ):
        entry_score = 0
        signals = []
        entry_signals = 0

        if ratio >= 1.10:
            entry_score += 40
            entry_signals += 1
            signals.append("[ENTRY] Extreme fear - Prime contrarian setup")
        elif ratio >= 1.05:
            entry_score += 35
            entry_signals += 1
            signals.append("[ENTRY] High fear - Strong entry signal")
        elif ratio >= 1.00:
            entry_score += 25
            entry_signals += 1
            signals.append("[ENTRY] Elevated fear - Entry signal")
        elif ratio >= 0.95:
            entry_score += 10
            signals.append("[WATCH] Neutral fear levels")
        else:
            entry_score += 0
            signals.append("[WAIT] Low fear - No contrarian edge")

        if rsi is not None:
            if rsi < 30:
                entry_score += 30
                entry_signals += 1
                signals.append("[ENTRY] RSI Oversold - Strong entry")
            elif rsi < 40:
                entry_score += 20
                entry_signals += 1
                signals.append("[ENTRY] RSI Approaching oversold")
            elif rsi < 50:
                entry_score += 10
                signals.append("[WATCH] RSI Neutral-low")
            elif rsi < 70:
                entry_score += 5
                signals.append("[WATCH] RSI Neutral-high")
            else:
                entry_score += 0
                signals.append("[WAIT] RSI Overbought - Wait")

        if macd_crossover == "bullish":
            entry_score += 20
            entry_signals += 1
            signals.append("[ENTRY] MACD Bullish - Momentum confirmed")
        elif macd_crossover == "neutral":
            entry_score += 5
            signals.append("[WATCH] MACD Neutral")
        else:
            entry_score += 0
            signals.append("[WAIT] MACD Bearish - Wait for turn")

        if above_ma200:
            entry_score += 20
            entry_signals += 1
            signals.append("[ENTRY] Above 200-MA - Bull trend")
        else:
            entry_score += 5
            signals.append("[WATCH] Below 200-MA - Caution")

        entry_score = max(0, min(100, entry_score))

        confidence = 50

        if ratio >= 1.10:
            confidence += 20
        elif ratio >= 1.00:
            confidence += 10
        elif ratio >= 0.95:
            confidence += 5
        else:
            confidence -= 5

        if rsi is not None:
            if rsi < 30:
                confidence += 20
            elif rsi < 40:
                confidence += 15
            elif rsi < 50:
                confidence += 5
            elif rsi < 70:
                confidence += 0
            else:
                confidence -= 10

        if macd_crossover == "bullish":
            confidence += 15
        elif macd_crossover == "neutral":
            confidence += 5
        else:
            confidence -= 5

        if above_ma200:
            confidence += 15
        else:
            confidence -= 10

        if entry_signals >= 3:
            confidence += 20
        elif entry_signals >= 2:
            confidence += 10
        elif entry_signals >= 1:
            confidence += 5
        else:
            confidence -= 15

        confidence = max(0, min(100, confidence))

        if entry_score >= 85 and entry_signals >= 3 and confidence >= 70:
            action = "STRONG BUY"
            color = "#22c55e"
        elif entry_score >= 65 and entry_signals >= 2 and confidence >= 60:
            action = "BUY"
            color = "#22c55e"
        elif entry_score >= 50 and confidence >= 70:
            action = "MODERATE BUY"
            color = "#84cc16"
        elif entry_score >= 40 or confidence >= 50:
            action = "WATCH"
            color = "#eab308"
        else:
            action = "WAIT"
            color = "#6b7280"

        return action, entry_score, confidence, color, signals, entry_signals

    def fetch_market_data(self):
        try:
            print("Fetching market data...")

            vix = yf.Ticker("^VIX")
            vix3m = yf.Ticker("^VIX3M")
            spy = yf.Ticker("^GSPC")

            vix_data = vix.history(period="5d")
            vix3m_data = vix3m.history(period="5d")
            spy_data = spy.history(period="1y")

            if vix_data.empty or vix3m_data.empty or spy_data.empty:
                raise ValueError("No market data available")

            vix_price = float(vix_data["Close"].iloc[-1])
            vix3m_price = float(vix3m_data["Close"].iloc[-1])
            spy_price = float(spy_data["Close"].iloc[-1])

            if vix_price <= 0 or vix3m_price <= 0 or spy_price <= 0:
                raise ValueError("Invalid price data")

            ratio = vix_price / vix3m_price

            prices_list = spy_data["Close"].tolist()
            prices_tuple = tuple(prices_list)

            rsi_value = self.calculate_rsi(prices_tuple, period=14)
            macd_line, signal_line = self.calculate_macd(prices_tuple)

            macd_crossover = "neutral"
            if macd_line is not None and signal_line is not None:
                if macd_line > signal_line:
                    macd_crossover = "bullish"
                elif macd_line < signal_line:
                    macd_crossover = "bearish"

            ma200_value = None
            above_ma200 = False
            if len(prices_list) >= 200:
                ma200_value = sum(prices_list[-200:]) / 200
                above_ma200 = spy_price > ma200_value

            return {
                "vix_price": vix_price,
                "vix3m_price": vix3m_price,
                "spy_price": spy_price,
                "ratio": ratio,
                "rsi": rsi_value,
                "macd_crossover": macd_crossover,
                "above_ma200": above_ma200,
                "ma200_value": ma200_value,
            }

        except Exception as e:
            print(f"Error fetching market data: {e}")
            return None

    def send_telegram_notification(
        self,
        signal_type,
        confidence,
        entry_score,
        ratio,
        vix_price,
        vix3m_price,
        spy_price,
    ):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if signal_type == "STRONG BUY":
                emoji = "🚨"
                urgency = "EXTREME ALERT"
            elif signal_type == "BUY":
                emoji = "📢"
                urgency = "BUY ALERT"
            else:
                return False

            message = f"""{emoji} {urgency} {emoji}

🎯 **Signal:** {signal_type}
📊 **Confidence:** {confidence}%
🏆 **Entry Score:** {entry_score}/100
📈 **VIX/VIX3M Ratio:** {ratio:.4f}
📉 **VIX:** {vix_price:.2f}
📉 **VIX3M:** {vix3m_price:.2f}
💰 **S&P 500:** ${spy_price:.2f}

⏰ **Time:** {timestamp}

🔔 Consider buying S&P 500 ETFs (SPY, VOO, IVV) when conditions align.

🤖 *Sent by Contrarian Edge 24/7 Monitor*"""

            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown",
            }

            response = requests.post(self.api_url, data=payload, timeout=10)
            response.raise_for_status()
            print(f"Telegram notification sent: {signal_type}")
            return True

        except Exception as e:
            print(f"Error sending Telegram notification: {e}")
            return False

    def check_and_notify(self):
        try:
            print(f"Checking market conditions at {datetime.now()}")

            market_data = self.fetch_market_data()
            if not market_data:
                print("Failed to fetch market data")
                return False

            signal_result = self.calculate_enhanced_signal(
                market_data["ratio"],
                market_data["vix_price"],
                market_data["rsi"],
                market_data["macd_crossover"],
                market_data["above_ma200"],
                market_data["spy_price"],
                market_data["ma200_value"],
            )

            signal_action, entry_score, confidence, color, signals, entry_signals = (
                signal_result
            )

            print(
                f"Current signal: {signal_action} (Score: {entry_score}, Confidence: {confidence}%)"
            )

            if (
                signal_action in ["BUY", "STRONG BUY"]
                and signal_action != self.last_signal
            ):
                print(f"New {signal_action} signal detected!")
                success = self.send_telegram_notification(
                    signal_action,
                    confidence,
                    entry_score,
                    market_data["ratio"],
                    market_data["vix_price"],
                    market_data["vix3m_price"],
                    market_data["spy_price"],
                )

                if success:
                    self.last_signal = signal_action
                    print(f"Notification sent for {signal_action}")
                else:
                    print("Failed to send notification")
            else:
                print(f"No new buy signal (current: {signal_action})")

            return True

        except Exception as e:
            print(f"Error in monitoring: {e}")
            return False


def main():
    print("🤖 Contrarian Edge 24/7 Monitor Starting...")

    try:
        monitor = ContrarianMonitor()
        success = monitor.check_and_notify()

        if success:
            print("✅ Monitoring cycle completed successfully")
        else:
            print("❌ Monitoring cycle failed")

    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
