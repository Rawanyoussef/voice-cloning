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

# تحديث pip وتثبيت wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# تثبيت numpy الإصدار المطلوب أولاً
RUN pip install --no-cache-dir numpy==1.22.0

# تثبيت PyTorch (CPU version)
RUN pip install --no-cache-dir \
    torch==2.1.0+cpu \
    torchaudio==2.1.0+cpu \
    --extra-index-url https://download.pytorch.org/whl/cpu

# تثبيت scipy
RUN pip install --no-cache-dir scipy==1.10.1

# تثبيت باقي المكتبات
RUN pip install --no-cache-dir -r requirements.txt

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


