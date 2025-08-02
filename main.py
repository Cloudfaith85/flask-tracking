from flask import Flask
from tracking import check_and_notify
import logging

app = Flask(__name__)

# Optional: Supaya log ditampilkan di console
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    logging.info("🔁 Checking tracking...")
    check_and_notify()
    return "✅ Tracking checked and notified (if updated)"

if __name__ == '__main__':
    # Jalankan di host='0.0.0.0' agar bisa diakses publik oleh UptimeRobot
    app.run(host='0.0.0.0', port=3000)