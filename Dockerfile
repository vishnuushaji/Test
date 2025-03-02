FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create storage directories
RUN mkdir -p /app/storage/processed_images \
             /app/storage/original_images \
             /app/storage/temp/uploads \
             /app/storage/temp/processing

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Add the entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]
# Default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]