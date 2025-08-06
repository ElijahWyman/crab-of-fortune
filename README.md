# 🦀 Crab of Fortune

A fun fortune-telling game featuring a friendly crab who predicts your future!

## Features
- Interactive fortune-telling experience
- Cute crab character
- Beach-themed interface
- Hover effects and smooth animations
- Random fortune generation
- Raspberry Pi compatible!

## Installation

### On Regular Computer
1. Make sure you have Python 3.x installed on your system
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### On Raspberry Pi
1. First, install required system packages:
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-pygame
```

2. Install SDL dependencies (if not already installed):
```bash
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```

## Running the Game

### On Regular Computer
To start the game, run:
```bash
python main.py
```

### On Raspberry Pi
1. Make sure you have X11 running:
```bash
echo $DISPLAY  # Should show :0 or similar
```

2. If X11 is not running, start it:
```bash
startx
```

3. Run the game:
```bash
python3 main.py
```

## Deploying to Raspberry Pi

### Method 1: Using SCP (Secure Copy)
1. From your development machine, use scp to copy the files:
```bash
scp -r /path/to/crab_of_fortune pi@raspberry_pi_ip:/home/pi/
```

### Method 2: Using Git
1. On your Raspberry Pi, install git:
```bash
sudo apt-get install git
```

2. Clone your repository:
```bash
git clone https://your-repository-url.git
cd crab_of_fortune
```

### Method 3: Using USB Drive
1. Copy the project folder to a USB drive
2. Plug the drive into your Raspberry Pi
3. Mount and copy the files:
```bash
sudo mount /dev/sda1 /mnt/usb  # Adjust device name as needed
cp -r /mnt/usb/crab_of_fortune ~/
```

## How to Play
1. Launch the game
2. Click the "Tell My Fortune!" button (or tap on touchscreen)
3. The wise crab will reveal your fortune in a message bubble
4. Click again for a new fortune!
5. Press ESC to exit the game

## Controls
- Click/tap the button to get a fortune
- Press ESC key or close window to exit
- Works with mouse, keyboard, or touchscreen

## Requirements
- Python 3.x
- Pygame 2.5.2
- For Raspberry Pi: SDL2 libraries

## Troubleshooting Raspberry Pi

If you encounter display issues:
1. Check if X11 is running:
```bash
echo $DISPLAY
```

2. If using SSH, enable X11 forwarding:
```bash
ssh -X pi@raspberry_pi_ip
```

3. For touchscreen issues:
```bash
sudo apt-get install xserver-xorg-input-evdev
sudo cp /usr/share/X11/xorg.conf.d/10-evdev.conf /usr/share/X11/xorg.conf.d/45-evdev.conf
```

4. For display driver issues:
```bash
sudo raspi-config
# Navigate to "Advanced Options" > "GL Driver" > Select "Full KMS"
``` 