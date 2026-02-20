# Backend Dockerfile
# FastAPI Todo API with Chatbot

# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Set environment variables
# - PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files
# - PYTHONUNBUFFERED: Ensures output is sent straight to terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 8000 for the FastAPI server
EXPOSE 8000

# Health check to ensure the service is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

# Run the application
# Using uvicorn as the ASGI server with hot reload disabled for production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
