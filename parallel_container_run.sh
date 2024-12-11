#!/bin/bash

# Function to display usage instructions
usage() {
  echo "Usage: $0 [playlist|video] [URL] [-t]"
  echo "  playlist    Download a YouTube playlist"
  echo "  video       Download a single YouTube video"
  echo "  -t          Enable transcription after downloading (optional)"
  exit 1
}

# Ensure at least two arguments are provided
if [ "$#" -lt 2 ]; then
  usage
fi

# Assign arguments to variables
DOWNLOAD_TYPE=$1
DOWNLOAD_URL=$2
ENABLE_TRANSCRIPTION="false"

# Check for the optional -t flag
if [ "$#" -eq 3 ] && [ "$3" = "-t" ]; then
  ENABLE_TRANSCRIPTION="true"
fi

# Export environment variables for use within Docker containers
export DOWNLOAD_URL
export ENABLE_TRANSCRIPTION

# Create a downloads directory if it doesn't exist
mkdir -p downloads

# Define the error log file path
ERROR_LOG_FILE="error_log.txt"

# Function to start a docker-compose service
start_service() {
  local service_dir=$1
  (
    cd "$service_dir" || exit
    docker-compose up -d 2>>"$ERROR_LOG_FILE"
  )
}

# Determine which service to start based on the download type
case $DOWNLOAD_TYPE in
  playlist)
    start_service "playlist_downloader"
    ;;
  video)
    start_service "video_downloader"
    ;;
  *)
    usage
    ;;
esac

# Wait for all background processes to finish
wait

# Reset ownership of the downloads directory to the current user
sudo chown -R "$(whoami):$(id -gn)" downloads
