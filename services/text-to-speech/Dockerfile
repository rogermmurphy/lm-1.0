# Text-to-Speech Service Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for Azure Speech SDK
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    build-essential \
    libssl-dev \
    ca-certificates \
    libasound2 \
    wget \
    && rm -rf /var/lib/apt/lists/*

COPY services/text-to-speech/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/python-common /tmp/lm-common
RUN pip install -e /tmp/lm-common

COPY services/text-to-speech/src/ ./src/

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
