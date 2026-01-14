# استخدام Python 3.10 كقاعدة
FROM python:3.10-slim

# تثبيت المكتبات الأساسية للنظام
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات
COPY requirements.txt .

# تثبيت مكتبات Python
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي الملفات
COPY run_tts.py .

# إنشاء المجلدات
RUN mkdir -p input output

COPY input/audio.wav /app/input/audio.wav

# تشغيل السكربت
CMD ["python", "run_tts.py"]