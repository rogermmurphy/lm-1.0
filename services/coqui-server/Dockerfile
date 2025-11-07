FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    TTS>=0.22.0 \
    flask>=3.0.0 \
    torch --index-url https://download.pytorch.org/whl/cpu

# Copy server code
COPY server.py /app/

# Expose port
EXPOSE 5002

# Run server
CMD ["python", "server.py"]
