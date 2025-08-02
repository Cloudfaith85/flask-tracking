import os
import requests
import datetime

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Tracking number bisa langsung di-hardcode di sini, atau baca dari file kalau mau
TRACKING_NUMBERS = ["E03160TRG"]  # Contoh

def fetch_status(tracking_number):
    try:
        url = f"https://api.beeconnectlogistics.com/track?awb={tracking_number}"
        headers = {
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        return data.get("result", {}).get("awb_status", "❌ Failed to retrieve status.")
    except Exception as e:
        return f"❌ Error fetching: {str(e)}"

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not CHAT_ID:
        print("Missing Telegram bot token or chat ID.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram error:", e)

def check_and_notify():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"📦 Tracking Update ({now}):\n\n"
    for awb in TRACKING_NUMBERS:
        status = fetch_status(awb)
        message += f"🔹 {awb}: {status}\n"
    send_telegram_message(message)
