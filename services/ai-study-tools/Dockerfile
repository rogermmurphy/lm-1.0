FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY services/ai-study-tools/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared library
COPY shared/python-common /shared/python-common
RUN pip install -e /shared/python-common

# Copy application code
COPY services/ai-study-tools/src /app/src
COPY services/ai-study-tools/.env /app/.env

# Expose port
EXPOSE 8009

# Run the application
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8009", "--reload"]
