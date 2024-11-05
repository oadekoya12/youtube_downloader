# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install ffmpeg and other dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create a directory for downloaded videos
RUN mkdir -p /downloads

# Set /downloads as a volume for storing downloaded videos
VOLUME /downloads
