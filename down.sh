#!/bin/bash

# Function to stop and remove a Docker container if it exists
manage_container() {
  local container_name=$1

  # Check if the container exists
  if [ "$(docker ps -a -q -f name=^${container_name}$)" ]; then
    # Check if the container is running
    if [ "$(docker ps -q -f name=^${container_name}$)" ]; then
      echo "Stopping running container: $container_name"
      docker stop "$container_name"
    else
      echo "Container $container_name is not running."
    fi
    echo "Removing container: $container_name"
    docker rm "$container_name"
  else
    echo "No container named $container_name found."
  fi
}

# Target containers
containers=("youtube-playlist-downloader" "youtube-video-downloader")

# Iterate over the list and manage each container
for container in "${containers[@]}"; do
  manage_container "$container"
done
