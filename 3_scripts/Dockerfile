# Python API için Dockerfile
FROM python:3.10-slim

# Çalışma dizini
WORKDIR /app

# Sistem bağımlılıkları (fontlar dahil)
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-dejavu-core \
    fonts-liberation \
    fontconfig \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && fc-cache -f -v

# Python bağımlılıkları
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyaları
COPY *.py .

# Output dizinini oluştur
RUN mkdir -p /app/output

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV ASSETS_DIR=/app/assets
ENV OUTPUT_DIR=/app/output
ENV API_BASE_URL=http://localhost:8000
ENV FONT_PATH=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf

# Port
EXPOSE 8000

# Sağlık kontrolü
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Başlatma komutu
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
