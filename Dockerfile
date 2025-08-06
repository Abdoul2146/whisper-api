FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
