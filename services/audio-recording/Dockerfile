# Audio Recording Service Dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc postgresql-client && rm -rf /var/lib/apt/lists/*

COPY services/audio-recording/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/python-common /tmp/lm-common
RUN pip install -e /tmp/lm-common

COPY services/audio-recording/src/ ./src/

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
