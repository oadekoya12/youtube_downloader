# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the shared requirements.txt from the parent directory
COPY requirements.txt .

# Update pip and setuptools to the latest versions
RUN pip install --upgrade pip setuptools

# Install ffmpeg and other dependencies
RUN apt-get update && apt-get install -y ffmpeg && \
    pip install --no-cache-dir -r requirements.txt

# Copy all necessary files and directories, including the script folder
COPY . .

# Create a directory for downloaded videos
RUN mkdir -p /downloads

# Set /downloads as a volume for storing downloaded videos
VOLUME /downloads
