#!/bin/sh

# Ensure the playlist URL is provided
if [ -z "$PLAYLIST_URL" ]; then
  echo "Error: PLAYLIST_URL environment variable is required."
  exit 1
fi

# Debugging: Output the transcription flag
echo "Transcription flag is set to: $ENABLE_TRANSCRIPTION"

# Conditionally run the download script with or without transcription
if [ "$ENABLE_TRANSCRIPTION" = "true" ]; then
  python download_playlist.py "$PLAYLIST_URL" -t
else
  python download_playlist.py "$PLAYLIST_URL"
fi
