# Use official Python 3.10 slim image as the base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Install the local package in editable mode
RUN pip install --no-cache-dir -e .

# Create directories needed at runtime
RUN mkdir -p prediction_output final_model

# Expose the port the app runs on
EXPOSE 8080

# Default environment variables (can be overridden at runtime)
ENV PORT=8080

# Run the FastAPI application
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]
