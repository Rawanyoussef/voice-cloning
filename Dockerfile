FROM python:3.10-slim

# System deps
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

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# install all deps in one shot (important)
RUN pip install --no-cache-dir -r requirements.txt

COPY run_tts.py .

RUN mkdir -p input output

ENV COQUI_TOS_AGREED=1

CMD ["python", "run_tts.py"]



