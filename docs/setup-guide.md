# 📖 دليل التثبيت والتشغيل

## المتطلبات
- Python 3.9+
- حساب Claude API
- حساب GitHub

## الخطوات

### 1. إعداد الخادم الوسيط
```bash
cd server
cp .env.example .env
# ضع مفتاح Claude API في ملف .env
pip install -r requirements.txt
python proxy-server.py