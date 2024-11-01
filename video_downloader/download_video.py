import os
import sys
from yt_dlp import YoutubeDL
from transcribe_script import main as transcribe_video  # Import transcription function

def download_single_video(video_url, output_dir):
    # Configure yt_dlp options
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    }

    with YoutubeDL(ydl_opts) as ydl:
        # Download the video
        print(f"Downloading video: {video_url}")
        video_info = ydl.extract_info(video_url, download=True)
        video_path = ydl.prepare_filename(video_info)
        print(f"Downloaded {video_path}")

        # Transcribe the downloaded video
        transcribe_video(video_path)
        print(f"Transcribed {video_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python download_video.py <video_url>")
        sys.exit(1)

    video_url = sys.argv[1]
    output_dir = "path/to/downloaded_videos"
    os.makedirs(output_dir, exist_ok=True)
    
    download_single_video(video_url, output_dir)

if __name__ == "__main__":
    main()
