# Use a minimal, official Python base image with slim version for reduced size
FROM python:3.12-slim

# Accept UUID and GUID as build arguments with no default values
ARG UUID=1000
ARG GUID=1000

# Create a group and user named 'python' with dynamic IDs passed during build
RUN addgroup --system --gid "$GUID" python && \
    adduser --system --uid "$UUID" --ingroup python python

# Create directories for downloaded videos and cache, then adjust permissions
RUN mkdir -p /downloads /cache && \
    chown -R python:python /downloads /cache && \
    chmod 755 /downloads /cache

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies and clean up cached files afterward
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker layer caching
COPY requirements.txt ./

# Upgrade pip to the latest version
# Install the latest version of yt-dlp
RUN pip install --upgrade pip && \
    pip install --no-cache-dir yt-dlp -r requirements.txt

# Install Python dependencies as root, then switch to the non-root user
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Set environment variable to specify cache location for yt-dlp
ENV XDG_CACHE_HOME=/cache

# Switch to the non-root user 'python' after installation
USER python
ENV HOME=/home/python

# Set /downloads as a volume for storing downloaded videos
VOLUME /downloads
# ENTRYPOINT ["/bin/sh", "-c", "mkdir -p /downloads && chown -R python:python /downloads && exec \"$@\""]

# Optional: Restrict container capabilities, depending on application needs
# `cap_drop=ALL` is a security measure that removes all Linux capabilities from the container.
# By default, Docker containers run with certain elevated capabilities (e.g., CAP_NET_RAW for low-level networking).
# Since this downloader application does not require elevated privileges, removing these capabilities reduces the security risk.
# Uncomment the following line if the container does not need elevated privileges
# --cap-drop=ALL
