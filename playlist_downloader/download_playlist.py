import os
import sys
import argparse
import warnings
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, ExtractorError

# Add the parent script directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../script")))
from transcribe_script import main as transcribe_video

# Suppress FP16 warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Define the path for the log file within a writable directory
log_file_path = os.path.join('/downloads', 'error_log.txt')

# Ensure the directory exists
os.makedirs('/downloads', exist_ok=True)

# Configure logging to write to the specified file
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'  # Open the log file in append mode
)

def download_and_transcribe(video_url, ydl_opts, transcribe):
    with YoutubeDL(ydl_opts) as ydl:
        try:
            logging.info(f"Downloading video: {video_url}")
            video_info = ydl.extract_info(video_url, download=True)
            video_path = ydl.prepare_filename(video_info)
            logging.info(f"Downloaded {video_path}")

            if transcribe:
                logging.info(f"Transcribing video: {video_path}")
                transcribe_video(video_path)
                logging.info(f"Transcription completed for {video_path}")
            else:
                logging.info("Skipping transcription.")

        except (DownloadError, ExtractorError) as e:
            logging.error(f"Error downloading video {video_url}: {e}")
            log_error(video_url, str(e))

def download_playlist(playlist_url, output_dir, transcribe=False, max_workers=4):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'ignoreerrors': True,  # Continue on download errors
        'quiet': True,
        'extractor_retries': 10,  # Increase the number of retries for extractor errors
        'verbose': True,  # Enable verbose logging
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            logging.info(f"Attempting to download playlist: {playlist_url}")
            info_dict = ydl.extract_info(playlist_url, download=False)

            video_urls = [
                entry.get('webpage_url') for entry in info_dict.get('entries', [])
                if entry and entry.get('webpage_url')
            ]

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(download_and_transcribe, url, ydl_opts, transcribe): url
                    for url in video_urls
                }

                for future in as_completed(futures):
                    url = futures[future]
                    try:
                        future.result()
                    except Exception as e:
                        logging.error(f"Error processing video {url}: {e}")
                        log_error(url, str(e))

        except (DownloadError, ExtractorError) as e:
            logging.error(f"Error processing playlist {playlist_url}: {e}")
            log_error(playlist_url, str(e))

def log_error(url, error_message):
    logging.error(f"URL: {url}\nError Details: {error_message}\n")
    print(f"Logged error for URL: {url}")

def main():
    parser = argparse.ArgumentParser(description="Download a YouTube playlist with optional transcription.")
    parser.add_argument("url", help="The URL of the YouTube playlist to download")
    parser.add_argument("-t", "--transcribe", action="store_true", help="Enable transcription after downloading each video")
    parser.add_argument("-w", "--workers", type=int, default=4, help="Number of parallel download/transcription workers")
    args = parser.parse_args()

    output_dir = "/downloads"
    os.makedirs(output_dir, exist_ok=True)

    download_playlist(args.url, output_dir, transcribe=args.transcribe, max_workers=args.workers)

if __name__ == "__main__":
    main()
