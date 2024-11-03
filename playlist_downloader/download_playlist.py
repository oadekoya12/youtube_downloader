import sys
import os

# Add the parent script directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../script")))

from yt_dlp import YoutubeDL
from transcribe_script import main as transcribe_video  # Corrected import path

def download_playlist(playlist_url, output_dir):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=False)
        for entry in info_dict['entries']:
            video_url = entry['webpage_url']
            print(f"Downloading video: {video_url}")

            video_info = ydl.extract_info(video_url, download=True)
            video_path = ydl.prepare_filename(video_info)
            print(f"Downloaded {video_path}")

            transcribe_video(video_path)
            print(f"Transcribed {video_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python download_playlist.py <playlist_url>")
        sys.exit(1)

    playlist_url = sys.argv[1]
    output_dir = "/downloads"
    os.makedirs(output_dir, exist_ok=True)

    download_playlist(playlist_url, output_dir)

if __name__ == "__main__":
    main()
