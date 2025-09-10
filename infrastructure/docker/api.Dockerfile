# API Service Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy shared requirements first for better caching
COPY shared/requirements.txt /usr/src/app/shared/requirements.txt

# Copy API specific requirements
COPY services/api/requirements.txt /usr/src/app/services/api/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r services/api/requirements.txt

# Copy shared module
COPY shared/ /usr/src/app/shared/

# Copy API service
COPY services/api/ /usr/src/app/services/api/

# Expose port
EXPOSE 8000

# Command will be specified in docker-compose
CMD ["uvicorn", "services.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
