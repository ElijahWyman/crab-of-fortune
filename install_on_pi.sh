#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Starting Crab of Fortune installation on Ubuntu 24 LTS...${NC}\n"

# Update package list
echo -e "${GREEN}Updating package list...${NC}"
sudo apt update

# Install required packages
echo -e "${GREEN}Installing required packages...${NC}"
sudo apt install -y \
    python3-pip \
    python3-pygame \
    python3-venv \
    cups \
    cups-daemon \
    cups-client \
    python3-cups \
    libcups2-dev \
    printer-driver-brlaser \
    libusb-1.0-0 \
    usbutils \
    espeak-ng \
    pulseaudio \
    pulseaudio-utils

# Set up CUPS
echo -e "${GREEN}Setting up CUPS...${NC}"
sudo usermod -a -G lpadmin $USER
sudo sed -i 's/Listen localhost:631/Port 631/' /etc/cups/cupsd.conf
sudo systemctl enable cups
sudo systemctl restart cups

# Wait for CUPS to start
echo -e "${GREEN}Waiting for CUPS to start...${NC}"
sleep 5

# Check CUPS status
echo -e "${GREEN}Checking CUPS status...${NC}"
lpstat -t || echo "No printers configured yet"

# Set up audio system
echo -e "${GREEN}Setting up audio system...${NC}"
sudo usermod -a -G audio $USER
sudo usermod -a -G pulse $USER
sudo usermod -a -G pulse-access $USER

# Configure audio
echo -e "${GREEN}Configuring audio...${NC}"
pactl set-sink-volume @DEFAULT_SINK@ 70%
pactl set-source-volume @DEFAULT_SOURCE@ 70%

# Create Python virtual environment
echo -e "${GREEN}Creating Python virtual environment...${NC}"
python3 -m venv venv
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
systemctl status cups
echo -e "\nPrinter Status:"
lpstat -t || echo "No printers configured yet"
echo -e "\nUSB Devices:"
lsusb
echo -e "\nUSB Permissions:"
ls -l /dev/usb/lp* 2>/dev/null || echo "No USB printer device found"
ls -l /dev/bus/usb/*/* 2>/dev/null

# Test brother_ql installation
echo -e "\n${GREEN}Testing brother_ql installation:${NC}"
brother_ql --version

# Test audio system
echo -e "\n${GREEN}Testing audio system:${NC}"
espeak-ng --version || echo "espeak-ng not found"
pactl list sinks short | head -1 || echo "No audio sinks found"

echo -e "\n${GREEN}Installation and setup complete!${NC}"