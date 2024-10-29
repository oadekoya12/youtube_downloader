import os
import yt_dlp

# Get the video URL from the environment variable
video_url = os.getenv('VIDEO_URL')

if not video_url:
    print('Error: VIDEO_URL environment variable is not set.')
    exit(1)

download_dir = '/downloads'

# Set up yt-dlp options
ydl_opts = {
    'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
    'format': 'best'
}

# Download the video using yt-dlp
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

print('Download process completed!')
