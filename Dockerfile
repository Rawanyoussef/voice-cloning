FROM python:3.10-slim

# تثبيت المكتبات النظامية الضرورية
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libsndfile1 \
    libsndfile1-dev \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# تعيين مجلد العمل
WORKDIR /app

# نسخ وتثبيت المتطلبات
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY run_tts.py .

# إنشاء المجلدات المطلوبة
RUN mkdir -p input output

# نسخ الملف الصوتي (اختياري - يمكن استخدام volume mounting بدلاً منه)
# COPY input/audio.wav /app/input/audio.wav

# تعيين متغير البيئة للموافقة على الترخيص
ENV COQUI_TOS_AGREED=1

# تشغيل السكريبت
CMD ["python", "run_tts.py"]
