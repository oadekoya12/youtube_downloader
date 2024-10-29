# YouTube Downloader

This project provides a flexible setup to download either an entire YouTube playlist or a single video using Docker and `yt-dlp`.

## Structure

- **playlist_downloader/**: Contains files for downloading a playlist.
- **video_downloader/**: Contains files for downloading a single video.
- **downloads/**: Shared directory for storing downloaded videos.
- **Dockerfile**: Shared Dockerfile for both playlist and video downloads.
- **requirements.txt**: Shared dependencies file.
- **download_script.sh**: Bash script to handle both playlist and single video downloads.

## Requirements

- Docker
- Docker Compose
- Bash (for running the script)
- WSL (for Windows users)
- macOS/Linux Terminal (for Mac or Linux users

## Environment Setup

### 1. Running on macOS or Linux

For Mac and any Linux distribution, follow these steps:

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
   - Run the following command to verify that Docker is installed and working:
     ```bash
     docker --version
     ```

### 2. Running on Windows Subsystem for Linux (WSL)

If you are using Windows, you can run this project using **WSL**. Follow these steps:

1. **Enable WSL**:
   - Open PowerShell as Administrator and run:
     ```powershell
     wsl --install
     ```
   - Restart your computer if prompted.

2. **Install Docker Desktop**:
   - Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop) for Windows.
   - Ensure that Docker Desktop is configured to run with WSL by enabling the "Use the WSL 2 based engine" option in Docker Desktop settings.

3. **Install Docker and Docker Compose in WSL**:
   - Open WSL and run:
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
   - Run the following command to verify that Docker is installed and working:
     ```bash
     docker --version
     ```

## How to Use

### 1. Make the script executable
Run the following command to make the script executable:
```bash
chmod +x download_script.sh
```
### 2. Run the script
#### Download a YouTube Playlist
To download a playlist, use:
```bash
./download_script.sh playlist "https://www.youtube.com/watch?v=VnvRFRk_51k&list=PLy7NrYWoggjziYQIDorlXjTvvwweTYoNC"
```
#### Download a Single YouTube Video
To download a single video, use:
```bash
./download_script.sh video "https://www.youtube.com/watch?v=VnvRFRk_51k"
```
## Description
The script (download_script.sh) automatically determines whether to download a YouTube playlist or a single video based on the command-line arguments.

## Example Commands
  - Download a playlist:
  ```bash
  ./download_script.sh playlist "https://www.youtube.com/watch?v=VnvRFRk_51k&list=[PLAYLIST_ID]"
  ```
  - Download a single video:
  ```bash
  ./download_script.sh video "https://www.youtube.com/[VIDEO_ID]"
  ```

## How It Works
 - The script uses Docker Compose to run a containerized environment for downloading the specified playlist or video.
 - The downloaded files will be stored in the shared downloads directory, making it accessible from the host machine.
 - Replace the placeholder to their corrsponding Vidoe or Playlist ID

 ## Troubleshooting
If you encounter any issues with permissions in the downloads directory, you can reset the ownership using:
```bash
sudo chown -R $(whoami):$(id -gn $USER) downloads
```

## Notes
- Ensure that Docker and Docker Compose are installed and running on your system.
- Use valid YouTube URLs for the download to work correctly.
- If using WSL, make sure Docker Desktop is running and integrated with WSL.

Let me know if you need any changes or additional content!