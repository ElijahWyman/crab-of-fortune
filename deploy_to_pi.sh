#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Configuration
PI_USER="superquarters"
PI_HOST="192.168.1.66"
LOCAL_DIR="/Users/elijahwyman/Downloads/crab_of_fortune"
REMOTE_DIR="/home/superquarters/crab_of_fortune"

# Test SSH connection
echo -e "${GREEN}Testing SSH connection to Raspberry Pi...${NC}"
ssh -o ConnectTimeout=5 $PI_USER@$PI_HOST "echo 'SSH connection successful'" || {
    echo -e "${RED}Could not connect to Raspberry Pi at $PI_HOST${NC}"
    echo "Please ensure:"
    echo "1. The Pi is powered on and connected to the network"
    echo "2. SSH is enabled on the Pi"
    echo "3. The IP address $PI_HOST is correct"
    echo "4. Your SSH key is set up on the Pi"
    exit 1
}

# Create remote directory
echo -e "${GREEN}Creating remote directory...${NC}"
ssh $PI_USER@$PI_HOST "mkdir -p $REMOTE_DIR"

# Copy files
echo -e "${GREEN}Copying files to Raspberry Pi...${NC}"
scp -r "$LOCAL_DIR"/* $PI_USER@$PI_HOST:$REMOTE_DIR/ || {
    echo -e "${RED}Failed to copy files to Raspberry Pi${NC}"
    exit 1
}

# Make install script executable and run it
echo -e "${GREEN}Running installation script on Raspberry Pi...${NC}"
ssh $PI_USER@$PI_HOST "chmod +x $REMOTE_DIR/install_on_pi.sh && $REMOTE_DIR/install_on_pi.sh"

echo -e "${GREEN}Deployment complete!${NC}"