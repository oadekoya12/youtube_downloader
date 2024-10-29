# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the shared requirements.txt from the parent directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the contents from the specific context directory
COPY . .

# Create a directory for downloaded videos
RUN mkdir -p /downloads

# Set the directory for downloads as a volume
VOLUME /downloads
