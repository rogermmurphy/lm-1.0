FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY services/class-management/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared library
COPY shared/python-common /shared/python-common
RUN pip install -e /shared/python-common

# Copy application code
COPY services/class-management/src /app/src
COPY services/class-management/src/config.py /app/src/config.py

# Expose port
EXPOSE 8005

# Run the application
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8005", "--reload"]
