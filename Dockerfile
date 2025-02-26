FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/outputs/audio /app/uploads

# Set environment variables
ENV PORT=7860
ENV DEBUG=False

# Expose the port
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]
