# Content Capture Service Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for OCR and PDF processing
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    poppler-utils \
    libpq-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY services/content-capture/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared common library
COPY shared/python-common /shared/python-common
RUN pip install -e /shared/python-common

# Copy service source code
COPY services/content-capture/src /app/src

# Create uploads directory
RUN mkdir -p /app/uploads

# Set environment variables
ENV PYTHONPATH=/app:/shared/python-common
ENV SERVICE_PORT=8008

# Expose port
EXPOSE 8008

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8008/health || exit 1

# Run the service
CMD ["python", "src/main.py"]
