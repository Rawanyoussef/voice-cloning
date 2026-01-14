FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY run_tts.py .

RUN mkdir -p input output
COPY input/audio.wav /app/input/audio.wav

EXPOSE 9500

CMD ["python", "run_tts.py"]
