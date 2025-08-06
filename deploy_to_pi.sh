#!/bin/bash

# Configuration
PI_USER="pi"
PI_HOST="raspberrypi.local"
REMOTE_DIR="/home/pi/crab_of_fortune"
LOCAL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Deploying Crab of Fortune to Raspberry Pi at $PI_HOST...${NC}"

# Check if we can reach the Pi using SSH
echo -e "\n${YELLOW}Testing connection to Raspberry Pi...${NC}"
if ! ssh $PI_USER@$PI_HOST "echo 'Connection test successful'" &> /dev/null; then
    echo -e "${RED}Could not connect to Raspberry Pi at $PI_HOST${NC}"
    exit 1
fi

# Create deployment directory on Pi
echo -e "\n${YELLOW}Creating directory on Raspberry Pi...${NC}"
ssh $PI_USER@$PI_HOST "mkdir -p $REMOTE_DIR" || {
    echo -e "${RED}Failed to create directory on Raspberry Pi${NC}"
    exit 1
}

# Copy files to Pi
echo -e "\n${YELLOW}Copying files to Raspberry Pi...${NC}"
scp -r "$LOCAL_DIR"/* $PI_USER@$PI_HOST:$REMOTE_DIR/ || {
    echo -e "${RED}Failed to copy files to Raspberry Pi${NC}"
    exit 1
}

# Copy the installation script
echo -e "\n${YELLOW}Copying and executing installation script...${NC}"
scp "$LOCAL_DIR/install_on_pi.sh" $PI_USER@$PI_HOST:$REMOTE_DIR/ || {
    echo -e "${RED}Failed to copy installation script${NC}"
    exit 1
}

# Make the installation script executable and run it
ssh $PI_USER@$PI_HOST "chmod +x $REMOTE_DIR/install_on_pi.sh && $REMOTE_DIR/install_on_pi.sh" || {
    echo -e "${RED}Failed to run installation script on Raspberry Pi${NC}"
    exit 1
}

echo -e "\n${GREEN}Deployment completed successfully!${NC}"
echo -e "${GREEN}You can now run the game on your Raspberry Pi with:${NC}"
echo -e "ssh $PI_USER@$PI_HOST"
echo -e "cd $REMOTE_DIR"
echo -e "python3 main.py" 