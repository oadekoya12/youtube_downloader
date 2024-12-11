import os
import sys
import argparse
import warnings
import logging
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

def download_video(url, output_dir, transcribe=False):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True,
        'extractor_retries': 10,  # Increase the number of retries for extractor errors
        'verbose': True,          # Enable verbose logging
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            logging.info(f"Attempting to download: {url}")
            video_info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(video_info)
            logging.info(f"Downloaded {video_path}")

            if transcribe:
                logging.info(f"Transcribing video: {video_path}")
                transcribe_video(video_path)
                logging.info(f"Transcription completed for {video_path}")
            else:
                logging.info("Skipping transcription.")

        except (DownloadError, ExtractorError) as e:
            logging.error(f"Error downloading URL {url}: {e}")
            log_error(url, str(e))
            sys.exit(1)

def log_error(url, error_message):
    logging.error(f"URL: {url}\nError Details: {error_message}\n")
    print(f"Logged error for URL: {url}")

def main():
    parser = argparse.ArgumentParser(description="Download a YouTube video with optional transcription.")
    parser.add_argument("url", help="The URL of the YouTube video to download")
    parser.add_argument("-t", "--transcribe", action="store_true", help="Enable transcription after downloading")
    args = parser.parse_args()

    output_dir = "/downloads"
    os.makedirs(output_dir, exist_ok=True)

    download_video(args.url, output_dir, transcribe=args.transcribe)

if __name__ == "__main__":
    main()
