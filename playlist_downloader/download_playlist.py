import os
import sys
from yt_dlp import YoutubeDL  # Import yt_dlp for downloading videos
from transcribe_script import main as transcribe_video  # Import the transcription function

def download_playlist(playlist_url, output_dir):
    """
    Downloads all videos from a YouTube playlist and transcribes each video.
    
    Args:
    playlist_url (str): URL of the YouTube playlist to download.
    output_dir (str): Directory where videos and transcripts will be saved.
    """

    # Configuration for yt_dlp
    ydl_opts = {
        'format': 'best',  # Download the best available quality
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # File path template for saving videos
    }

    # Initialize the YoutubeDL instance with the defined options
    with YoutubeDL(ydl_opts) as ydl:
        # Extract information about the playlist without downloading
        info_dict = ydl.extract_info(playlist_url, download=False)

        # Iterate through each video entry in the playlist
        for entry in info_dict['entries']:
            video_url = entry['webpage_url']  # Get each video's URL
            print(f"Downloading video: {video_url}")

            # Download the video and get video information
            video_info = ydl.extract_info(video_url, download=True)
            # Prepare filename based on downloaded video info
            video_path = ydl.prepare_filename(video_info)
            print(f"Downloaded {video_path}")

            # Call the transcription function on the downloaded video
            transcribe_video(video_path)
            print(f"Transcribed {video_path}")

def main():
    # Ensure the playlist URL is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python download_playlist.py <playlist_url>")
        sys.exit(1)

    # Get the playlist URL from command-line argument
    playlist_url = sys.argv[1]
    # Set output directory for downloads and transcripts
    output_dir = "path/to/downloaded_videos"
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
    
    # Run the download and transcription process for the playlist
    download_playlist(playlist_url, output_dir)

if __name__ == "__main__":
    main()
