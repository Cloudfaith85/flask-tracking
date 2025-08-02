import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

# === SETUP TELEGRAM BOT ===
TELEGRAM_TOKEN = "8254245198:AAHoMBs2zER_rVmvGBRKVE4iw2TYtz-RV5g"  # <- ganti dgn token asli kamu
CHAT_ID = "5921102036"                                              # <- ganti dgn chat id kamu

def now_jakarta():
    return datetime.now(ZoneInfo("Asia/Jakarta"))

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Telegram message sent!")
        else:
            print("❌ Failed to send:", response.text)
    except Exception as e:
        print("❌ Telegram error:", e)

def get_latest_status(tracking_number):
    url = "http://193.112.169.101:8082/en/trackIndex.htm"
    try:
        response = requests.post(url, data={"documentCode": tracking_number}, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        if not table:
            return None

        rows = table.find_all("tr")
        if len(rows) < 2:
            return None

        # Ambil baris pertama SETELAH header (rows[1] adalah status terbaru)
        status_row = rows[1]
        cols = status_row.find_all(["td", "th"])
        status_text = " | ".join(col.get_text(strip=True) for col in cols)
        return status_text
    except Exception as e:
        print("❌ Error fetching status:", e)
        return None

def check_and_notify():
    tracking_number = "E03160TRG"
    status_file = f"last_status_{tracking_number}.txt"

    if os.path.exists(status_file):
        with open(status_file, "r") as f:
            last_saved_status = f.read().strip()
    else:
        last_saved_status = ""

    latest_status = get_latest_status(tracking_number)

    if latest_status is None:
        print("❌ Failed to retrieve status.")
        return

    now_str = now_jakarta().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now_str}] 📦 Latest status:", latest_status)

    if latest_status != last_saved_status:
        send_telegram_message(f"📦 Update for {tracking_number}:\n{latest_status}")
        with open(status_file, "w") as f:
            f.write(latest_status)
    else:
        print("ℹ️ No update. Status unchanged.")

# Jalankan saat script dieksekusi langsung
if __name__ == "__main__":
    check_and_notify()