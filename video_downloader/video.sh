#!/bin/sh

# Ensure the video URL is provided
if [ -z "$VIDEO_URL" ]; then
  echo "Error: VIDEO_URL environment variable is required."
  exit 1
fi

# Debugging: Output the transcription flag
echo "Transcription flag is set to: $ENABLE_TRANSCRIPTION"

# Conditionally run the download script with or without transcription
if [ "$ENABLE_TRANSCRIPTION" = "true" ]; then
  python download_video.py "$VIDEO_URL" -t
else
  python download_video.py "$VIDEO_URL"
fi
