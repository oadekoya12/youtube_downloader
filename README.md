
# YouTube Downloader

This project provides a flexible setup to download either an entire YouTube playlist or a single video using Docker and `yt-dlp`.

**Disclaimer**: This tool is intended for **personal use only** with YouTube assets that you own or have permission to manage. Unauthorized downloading of content you do not own may violate YouTube’s Terms of Service. Please use responsibly and respect intellectual property rights.

**Docker Image**: The project Docker image can be pulled from Docker Hub at [hillseditor/dl_yt](https://hub.docker.com/r/hillseditor/dl_yt).

## Project Structure

- **playlist_downloader/**: Contains files for downloading a playlist.
  - `docker-compose.yml`: Docker Compose file for the `playlist_downloader` service.
  - `playlist.sh`: Shell script to handle the playlist download logic.
- **video_downloader/**: Contains files for downloading a single video.
  - `docker-compose.yml`: Docker Compose file for the `video_downloader` service.
  - `video.sh`: Shell script to handle the single video download logic.
- **downloads/**: Shared directory for storing downloaded videos and transcripts.
- **script/**: Contains `transcribe_script.py` for transcription functionality.
- **Dockerfile**: Shared Dockerfile for both playlist and video downloads.
- **requirements.txt**: Shared dependencies file.
- **.script**: Bash script to initiate both playlist and single video downloads, with an optional transcription flag.

## Requirements

- **Docker**
- **Docker Compose**
- **Bash** (for running the script)
- **WSL** (for Windows users)
- **macOS/Linux Terminal** (for Mac or Linux users)

## Usage Instructions

For any issues or suggestions regarding this project, please submit them here: [github.com/oadekoya12/youtube_downloader/issues](https://github.com/oadekoya12/youtube_downloader/issues).

For more about my work and services, visit my website: [www.hillseditorservices.com](https://www.hillseditorservices.com/).

---

## Environment Setup

### 1. Running on macOS or Linux

1. **Install Docker and Docker Compose**:
   - On **Mac**, download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop) and install it.
   - On **Linux**, use your package manager to install Docker and Docker Compose:
     ```bash
     sudo apt update           # For Debian/Ubuntu-based systems
     sudo apt install docker.io docker-compose
     ```
   - Add your user to the Docker group (on Linux):
     ```bash
     sudo usermod -aG docker $USER
     ```
   - Restart your terminal session to apply the changes.

2. **Verify Docker Installation**:
   ```bash
   docker --version
   ```

### 2. Running on Windows Subsystem for Linux (WSL)

1. **Enable WSL**:
   - Open PowerShell as Administrator and run:
     ```powershell
     wsl --install
     ```
   - Restart your computer if prompted.

2. **Install Docker Desktop**:
   - Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop) for Windows.
   - Enable "Use the WSL 2 based engine" in Docker Desktop settings.

3. **Install Docker and Docker Compose in WSL**:
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose
   ```
   - Add your user to the Docker group:
     ```bash
     sudo usermod -aG docker $USER
     ```
   - Restart WSL to apply the changes.

4. **Verify Docker Installation**:
   ```bash
   docker --version
   ```

## How to Use

### 1. Make the script executable
```bash
chmod +x .script
```

### 2. Run the script

#### Download a YouTube Playlist
```bash
./.script playlist "https://www.youtube.com/playlist?list=${PLAYLIST_ID}"
```

#### Download a Single YouTube Video
```bash
./.script video "https://www.youtube.com/watch?v=${VIDEO_ID}"
```

#### Process Local Videos for Transcription
```bash
./.script local "./downloads/transcribe/"
```

## Description
The `.script` file automatically determines whether to download a YouTube playlist or a single video based on the command-line arguments. It also supports an optional transcription flag (`-t`) for both types of downloads.

### Example Commands
  - Download a playlist:
    ```bash
    ./.script playlist "https://www.youtube.com/playlist?list=${PLAYLIST_ID}"
    ```
  - Download a single video:
    ```bash
    ./.script video "https://www.youtube.com/watch?v=${VIDEO_ID}"
    ```
  - Process Local Videos for Transcription:
    ```bash
    ./.script local "./downloads/transcribe/"
    ```
  - To extract transcripts from audio files:
    ```bash
    ./.script audio "./downloads/audio/"
    ```
## How It Works

- The `.script` uses Docker Compose to run a containerized environment for downloading the specified playlist or video.
- The downloaded files are stored in the shared `downloads` directory, accessible from the host machine.
- Replace `${PLAYLIST_ID}` or `${VIDEO_ID}` in commands with actual YouTube playlist or video IDs.

### Troubleshooting

If you encounter permission issues in the `downloads` directory, you can reset ownership with:
```bash
sudo chown -R $(whoami):$(id -gn $USER) downloads
```

## Notes

- Ensure Docker and Docker Compose are installed and running on your system.
- Use valid YouTube URLs for successful downloads.
- If using WSL, make sure Docker Desktop is running and integrated with WSL.

---

## License

MIT License

## Project Updates

**November 21, 2024**

- **Enhanced Error Handling:** Improved the application's ability to gracefully handle and log errors, especially when encountering private or hidden videos within playlists. This ensures uninterrupted processing of available videos.

- **Logging Enhancements:** Updated the logging mechanism to direct error logs to `error_log.txt` within the `/downloads` directory. This change resolves previous permission issues and ensures that logs are properly recorded.

