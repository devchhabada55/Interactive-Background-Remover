# Use the official Python 3.10 image as the base
FROM python:3.10-slim

# Set environment variables to prevent Python from buffering logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN apt-get update && \
    apt-get install -y gcc libgl1-mesa-glx && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . /app

# Expose the application port
EXPOSE 8080

# Set the entry point to run the Flask app
CMD ["python", "app.py"]
