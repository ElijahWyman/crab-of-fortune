#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Starting Crab of Fortune installation on Ubuntu Core...${NC}\n"

# Install required snaps
echo -e "${GREEN}Installing required snaps...${NC}"
sudo snap install python3
sudo snap install cups
sudo snap install usbutils

# Enable CUPS
echo -e "${GREEN}Setting up CUPS...${NC}"
sudo snap connect cups:raw-usb
sudo snap connect cups:network
sudo snap start cups

# Wait for CUPS to start
echo -e "${GREEN}Waiting for CUPS to start...${NC}"
sleep 5

# Create Python virtual environment using snap python
echo -e "${GREEN}Creating Python virtual environment...${NC}"
/snap/bin/python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo -e "${GREEN}Installing Python dependencies...${NC}"
pip install -r requirements.txt
pip install brother_ql

# Create launcher script
echo -e "${GREEN}Creating launcher script...${NC}"
cat > run_game.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 main.py
EOF
chmod +x run_game.sh

echo -e "${GREEN}Installation completed successfully!${NC}"
echo "You can now run the game with:"
echo "./run_game.sh"

# Final status check
echo -e "\n${GREEN}Final Status Check:${NC}"
echo "CUPS Status:"
snap services cups
echo -e "\nUSB Devices:"
/snap/bin/lsusb
echo -e "\nUSB Permissions:"
ls -l /dev/usb/lp* 2>/dev/null || echo "No USB printer device found"
ls -l /dev/bus/usb/*/* 2>/dev/null

# Test brother_ql installation
echo -e "\n${GREEN}Testing brother_ql installation:${NC}"
brother_ql --version

echo -e "\n${GREEN}Installation and setup complete!${NC}"
