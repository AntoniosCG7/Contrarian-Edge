import requests
import json
import os
from datetime import datetime


def test_telegram_connection():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("❌ Telegram credentials not found in environment variables")
        print("Make sure you've set up GitHub Secrets:")
        print("- TELEGRAM_BOT_TOKEN")
        print("- TELEGRAM_CHAT_ID")
        return False

    print(f"✅ Found credentials:")
    print(f"   Bot Token: {bot_token[:10]}...")
    print(f"   Chat ID: {chat_id}")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    test_message = f"""🧪 **TEST NOTIFICATION** 🧪

This is a test message from Contrarian Edge 24/7 Monitor.

⏰ **Time:** {timestamp}

🤖 *Sent by Contrarian Edge Test Script*"""

    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": test_message, "parse_mode": "Markdown"}

    try:
        print("📤 Sending test message...")
        response = requests.post(api_url, data=payload, timeout=10)
        response.raise_for_status()

        print("✅ Test message sent successfully!")
        print("📱 Check your Telegram for the test notification!")
        return True

    except Exception as e:
        print(f"❌ Error sending test message: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Testing Telegram Connection...")
    success = test_telegram_connection()

    if success:
        print("\n🎉 Telegram test completed successfully!")
    else:
        print("\n❌ Telegram test failed!")
