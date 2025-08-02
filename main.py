from flask import Flask
from tracking import check_and_notify

app = Flask(__name__)

@app.route('/')
def home():
    check_and_notify()
    return "✅ Tracking checked"

# Tidak perlu app.run() — karena akan dipanggil pakai gunicorn
