# POC 11.1: Coqui TTS Docker Setup
# Use official Coqui TTS image to avoid C++ compilation issues on Windows

FROM ghcr.io/coqui-ai/tts-cpu:latest

# Set working directory
WORKDIR /app

# Copy test scripts
COPY coqui_tts.py .
COPY benchmark_coqui.py .

# Install any additional dependencies
RUN pip install python-dotenv

# Expose port for potential server use
EXPOSE 5002

# Default command
CMD ["python", "coqui_tts.py"]
