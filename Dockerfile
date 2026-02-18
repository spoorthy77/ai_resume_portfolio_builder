# Multi-stage build for efficient Docker image
FROM python:3.11-slim as backend-builder

WORKDIR /app

# Install system dependencies including Fortran for scipy
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install Node.js from official repository
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application code
COPY . .

# Install frontend dependencies
WORKDIR /app/frontend
RUN npm install --production

# Set working directory back to root
WORKDIR /app

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Start the application
CMD ["python", "app.py"]
