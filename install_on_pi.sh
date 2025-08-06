#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${YELLOW}Starting Crab of Fortune installation on Raspberry Pi...${NC}"

# Update package list
echo -e "\n${YELLOW}Updating package list...${NC}"
sudo apt-get update || {
    echo -e "${RED}Failed to update package list${NC}"
    exit 1
}

# Install required packages
echo -e "\n${YELLOW}Installing required packages...${NC}"
sudo apt-get install -y python3-pip python3-pygame python3-venv || {
    echo -e "${RED}Failed to install required packages${NC}"
    exit 1
}

# Create virtual environment
echo -e "\n${YELLOW}Creating Python virtual environment...${NC}"
python3 -m venv "${SCRIPT_DIR}/venv" || {
    echo -e "${RED}Failed to create virtual environment${NC}"
    exit 1
}

# Activate virtual environment and install dependencies
echo -e "\n${YELLOW}Installing Python dependencies in virtual environment...${NC}"
source "${SCRIPT_DIR}/venv/bin/activate"
pip install -r "${SCRIPT_DIR}/requirements.txt" || {
    echo -e "${RED}Failed to install Python dependencies${NC}"
    deactivate
    exit 1
}
deactivate

# Check if X11 is running
echo -e "\n${YELLOW}Checking X11 status...${NC}"
if [ -z "$DISPLAY" ]; then
    echo -e "${YELLOW}X11 is not running. You may need to run 'startx' before running the game.${NC}"
fi

# Make main.py executable
chmod +x "${SCRIPT_DIR}/main.py" || {
    echo -e "${RED}Failed to make main.py executable${NC}"
    exit 1
}

# Create a launcher script
echo -e "\n${YELLOW}Creating launcher script...${NC}"
cat > "${SCRIPT_DIR}/run_game.sh" << EOL
#!/bin/bash
cd "$(dirname "\$0")"
source venv/bin/activate
python3 main.py
deactivate
EOL

chmod +x "${SCRIPT_DIR}/run_game.sh" || {
    echo -e "${RED}Failed to make launcher script executable${NC}"
    exit 1
}

echo -e "\n${GREEN}Installation completed successfully!${NC}"
echo -e "${GREEN}You can now run the game with:${NC}"
echo -e "./run_game.sh"
echo -e "\n${YELLOW}Note: If you see a blank screen, try:${NC}"
echo -e "1. Run 'startx' first"
echo -e "2. Make sure you're running on the Pi's desktop environment"
echo -e "3. Check the README.md for troubleshooting tips" 