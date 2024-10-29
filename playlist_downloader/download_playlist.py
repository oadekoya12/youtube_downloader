import os
import yt_dlp

# Get the playlist URL from the environment variable
playlist_url = os.getenv('PLAYLIST_URL')

if not playlist_url:
    print('Error: PLAYLIST_URL environment variable is not set.')
    exit(1)

download_dir = '/downloads'

# Set up yt-dlp options
ydl_opts = {
    'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
    'format': 'best'
}

# Download the playlist using yt-dlp
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist_url])

print('Download process completed!')
