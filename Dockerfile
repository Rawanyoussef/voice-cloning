FROM python:3.10-slim

# 1. Install System Dependencies
# بنسطب الحاجات دي عشان مكتبات الصوت تشتغل
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libsndfile1 \
    libsndfile1-dev \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Upgrade pip first (مهم جداً)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 3. Copy requirements and install
COPY requirements.txt .

# بنسطب المكتبات كلها مرة واحدة
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the code
COPY run_tts.py .
RUN mkdir -p input output

# 5. Environment Variables
ENV COQUI_TOS_AGREED=1

CMD ["python", "run_tts.py"]


