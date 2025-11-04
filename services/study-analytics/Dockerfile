FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY services/study-analytics/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install shared library
COPY shared/python-common /tmp/lm-common
RUN pip install --no-cache-dir /tmp/lm-common && rm -rf /tmp/lm-common

# Copy application code
COPY services/study-analytics/src ./src

# Expose port
EXPOSE 8012

# Run the application
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8012"]
