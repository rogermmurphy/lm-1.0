# Async Jobs Service Dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc postgresql-client && rm -rf /var/lib/apt/lists/*

COPY services/async-jobs/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/python-common /tmp/lm-common
RUN pip install -e /tmp/lm-common

COPY services/async-jobs/src/ ./src/

CMD ["python", "src/worker.py"]
