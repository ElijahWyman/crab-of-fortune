#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PI_USER="pi"
PI_HOST="raspberrypi.local"

echo -e "${YELLOW}Setting up SSH key authentication...${NC}"

# Create SSH key if it doesn't exist
if [ ! -f ~/.ssh/id_rsa ]; then
    echo -e "\n${YELLOW}Generating SSH key...${NC}"
    ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
fi

# Display instructions
echo -e "\n${YELLOW}Now copying your SSH key to the Raspberry Pi...${NC}"
echo -e "When prompted, enter the password: pi"

# Copy SSH key to Pi
ssh-copy-id -o StrictHostKeyChecking=no ${PI_USER}@${PI_HOST}

echo -e "\n${GREEN}SSH key setup completed!${NC}"
echo -e "${GREEN}You can now use the deploy script without entering a password.${NC}" 