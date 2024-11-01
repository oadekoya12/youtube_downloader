import os
import sys
from yt_dlp import YoutubeDL  # Import yt_dlp for downloading a single video
from transcribe_script import main as transcribe_video  # Import the transcription function

def download_single_video(video_url, output_dir):
    """
    Downloads a single video from YouTube and transcribes it.
    
    Args:
    video_url (str): URL of the YouTube video to download.
    output_dir (str): Directory where video and transcript will be saved.
    """

    # Configuration for yt_dlp
    ydl_opts = {
        'format': 'best',  # Download the best available quality
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # File path template for saving video
    }

    # Initialize the YoutubeDL instance with the defined options
    with YoutubeDL(ydl_opts) as ydl:
        # Download the video and get video information
        print(f"Downloading video: {video_url}")
        video_info = ydl.extract_info(video_url, download=True)
        # Prepare filename based on downloaded video info
        video_path = ydl.prepare_filename(video_info)
        print(f"Downloaded {video_path}")

        # Call the transcription function on the downloaded video
        transcribe_video(video_path)
        print(f"Transcribed {video_path}")

def main():
    # Ensure the video URL is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python download_video.py <video_url>")
        sys.exit(1)

    # Get the video URL from command-line argument
    video_url = sys.argv[1]
    # Set output directory for download and transcript
    output_dir = "path/to/downloaded_videos"
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
    
    # Run the download and transcription process for the single video
    download_single_video(video_url, output_dir)

if __name__ == "__main__":
    main()
