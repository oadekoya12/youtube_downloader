import os
import sys
import argparse
import warnings
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

# Add the parent script directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../script")))
from transcribe_script import main as transcribe_video

# Suppress FP16 warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

def download_playlist(playlist_url, output_dir, transcribe=False):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"Attempting to download playlist: {playlist_url}")
            info_dict = ydl.extract_info(playlist_url, download=False)

            for entry in info_dict['entries']:
                video_url = entry['webpage_url']
                print(f"Downloading video: {video_url}")
                
                try:
                    video_info = ydl.extract_info(video_url, download=True)
                    video_path = ydl.prepare_filename(video_info)
                    print(f"Downloaded {video_path}")

                    # Transcribe in chunks if the flag is set to True
                    if transcribe:
                        print(f"Transcribing video in chunks for {video_path}...")
                        transcribe_video(video_path)
                        print(f"Transcription completed for {video_path}")
                    else:
                        print("Skipping transcription.")

                except DownloadError as e:
                    print(f"Error encountered for video URL: {video_url}")
                    log_error(video_url, str(e))

        except DownloadError as e:
            print(f"Error encountered for playlist URL: {playlist_url}")
            log_error(playlist_url, str(e))

def log_error(url, error_message):
    with open("download.log", "a") as log_file:
        log_file.write(f"URL: {url}\nError Details: {error_message}\n\n")
    print(f"Logged error for URL: {url}")

def main():
    parser = argparse.ArgumentParser(description="Download a YouTube playlist with optional transcription.")
    parser.add_argument("url", help="The URL of the YouTube playlist to download")
    parser.add_argument("-t", "--transcribe", action="store_true", help="Enable transcription after downloading each video")
    args = parser.parse_args()

    output_dir = "/downloads"
    os.makedirs(output_dir, exist_ok=True)

    # Ensure transcription is only triggered when the -t flag is passed
    download_playlist(args.url, output_dir, transcribe=args.transcribe)

if __name__ == "__main__":
    main()
