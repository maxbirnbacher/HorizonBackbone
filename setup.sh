#!/bin/bash

# Get the system's IP address
IP=$(hostname -I | awk '{print $2}')

# Replace localhost with the system's IP address in the main.py files
sed -i "s/localhost/$IP/g" c2-api/main.py
sed -i "s/localhost/$IP/g" file-api/main.py
sed -i "s/localhost/$IP/g" user-api/main.py

# debug output
cat c2-api/main.py | grep "$IP"

echo "Welcome to the setup script for HorizonBackbone"
echo "This script will build the docker images and start the containers"
echo "Please make sure you have docker(-compose) or podman(-compose) installed"

if command -v docker &>/dev/null; then
  echo "Using docker"
  cd horizon-frontend && docker build -t horizon-frontend . && cd ..
  cd c2-api && docker build -t c2-api . && cd ..
  cd user-api && docker build -t user-api . && cd ..
  cd file-api && docker build -t file-api . && cd ..
  docker-compose up
elif command -v podman &>/dev/null; then
  echo "Using podman"
  cd horizon-frontend && podman build -t horizon-frontend . && cd ..
  cd c2-api && podman build -t c2-api . && cd ..
  cd user-api && podman build -t user-api . && cd ..
  cd file-api && podman build -t file-api . && cd ..
  podman-compose up
else
  echo "Neither docker nor podman is available"
fi