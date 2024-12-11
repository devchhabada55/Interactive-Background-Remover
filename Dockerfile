# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /OnlineSalesAI

# Copy application files to the correct directory
COPY . /OnlineSalesAI

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 8080

# Define environment variables
ENV OUTPUT_DIR="/OnlineSalesAI/static"

# Command to run the app
CMD ["python", "app.py"]
