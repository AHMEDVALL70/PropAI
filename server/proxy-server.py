# proxy-server.py
# خادم وسيط آمن لتطبيق أحمد فال PropAI

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# 🔑 المفتاح يُحفظ كمتغير بيئة (آمن)
CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY', 'YOUR_API_KEY_HERE')
ANTHROPIC_URL = 'https://api.anthropic.com/v1/messages'

SYSTEM_PROMPT_AR = """أنت مستشار عقاري خبير متخصص في سوق العقارات بدولة قطر لعام 2026. 
لديك معرفة بأسعار: لوسيل(13800ر.ق/م²)، اللؤلؤة(16500)، المشيرب(15000)، الريان(11200)، 
الوكرة(9500)، الخليج الغربي(18000). العوائد الإيجارية 5-7.5%. 
أجب بالعربية بشكل مهني ومختصر مع أرقام دقيقة."""

SYSTEM_PROMPT_EN = """You are an expert real estate advisor specializing in Qatar's 2026 property market. 
You know prices: West Bay(18000 QAR/m²), Pearl(16500), Musheireb(15000), Lusail(13800), 
Al Rayyan(11200), Al Wakra(9500). Rental yields 5-7.5%. 
Respond professionally in English with precise figures."""

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        message = data.get('message', '')
        language = data.get('language', 'ar')
        history = data.get('history', [])
        
        system_prompt = SYSTEM_PROMPT_AR if language == 'ar' else SYSTEM_PROMPT_EN
        
        messages = []
        for msg in history:
            messages.append({
                'role': msg.get('role', 'user'),
                'content': msg.get('content', '')
            })
        messages.append({'role': 'user', 'content': message})
        
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': CLAUDE_API_KEY,
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            'model': 'claude-3-5-sonnet-20240620',
            'max_tokens': 1000,
            'system': system_prompt,
            'messages': messages
        }
        
        response = requests.post(ANTHROPIC_URL, headers=headers, json=payload)
        
        if response.status_code != 200:
            return jsonify({'error': f'Claude API error: {response.status_code}'}), 500
        
        result = response.json()
        reply = result.get('content', [{}])[0].get('text', '⚠️ لم يتم الحصول على رد')
        
        return jsonify({'reply': reply})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Proxy server is running'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)