# 🦀 Crab of Fortune - Multi-Realms of Wisdom

A mystical, interactive fortune-telling experience designed for Raspberry Pi, featuring beautiful artwork, text-to-speech, and three distinct realms of wisdom.

## ✨ Features

### 🎭 Multi-Page Interface
- **START Screen**: Beautiful artwork with invisible click zones
- **Turtle Realm**: Numerology and angel number messages
- **Crab Realm**: Deep spiritual wisdom and guidance
- **Rat Realm**: Passionate love readings and romantic insights

### 🎤 Audio System
- **Different Voices**: Each animal has a unique voice personality
- **Immediate Playback**: No delays, audio starts instantly
- **Text-to-Speech**: Uses `spd-say` for reliable audio on Raspberry Pi
- **Voice Characteristics**:
  - 🐢 **Turtle**: Slow, wise, deep female voice
  - 🦀 **Crab**: Mystical, medium-paced male voice
  - 🐀 **Rat**: Passionate, comfortable-paced female voice

### 🖼️ Visual Experience
- **Fullscreen Mode**: Borderless, immersive display
- **Dynamic Scaling**: Automatically fits any screen resolution
- **Beautiful Artwork**: High-quality background images for each realm
- **Clean Interface**: No cluttered buttons, pure art experience

### ⏰ User Experience
- **20-Second Timer**: Comfortable time to absorb each message
- **Auto-Return**: Automatically returns to choice screen
- **Invisible Click Zones**: Art remains visible while being interactive
- **ESC Key**: Easy exit from fullscreen mode

## 🚀 Installation

### Prerequisites
- Raspberry Pi running Ubuntu LTS
- Python 3.8+
- Pygame library
- Audio system with `spd-say` support

### Quick Setup
1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd crab_of_fortune
   ```

2. **Deploy to Raspberry Pi**:
   ```bash
   ./deploy_to_pi.sh
   ```

3. **Run the game**:
   ```bash
   ssh superquarters@192.168.1.66
   cd crab_of_fortune
   source venv/bin/activate
   python3 main.py
   ```

## 🎮 How to Play

1. **Start Screen**: Click on any of the three animals (Turtle, Crab, or Rat)
2. **Fortune Display**: Your fortune appears immediately with audio
3. **Listen & Read**: Absorb the wisdom for 20 seconds
4. **Auto-Return**: Automatically returns to choice screen
5. **Choose Again**: Select a different animal for new insights
6. **Exit**: Press ESC key to quit

## 🏗️ Project Structure

```
crab_of_fortune/
├── main.py                 # Main game logic and interface
├── fortune_speaker.py      # Text-to-speech system
├── fortunes.py             # Crab realm spiritual fortunes
├── turtle_fortunes.py      # Turtle realm numerology messages
├── rat_fortunes.py         # Rat realm love readings
├── deploy_to_pi.sh         # Deployment script for Raspberry Pi
├── install_on_pi.sh        # Pi setup and dependency installation
├── requirements.txt        # Python dependencies
├── START.jpg              # Main menu background
├── turtle.jpg             # Turtle realm background
├── crab.jpg               # Crab realm background
├── rat.jpg                # Rat realm background
└── README.md              # This file
```

## 🔧 Technical Details

### Audio System
- **Primary Engine**: `spd-say` (Speech Dispatcher)
- **Fallback Engines**: `espeak`, `festival`
- **Voice Control**: Rate, pitch, and voice type customization
- **Volume Management**: Automatic 70% volume setting

### Display System
- **Resolution Detection**: Automatic screen size detection
- **Image Scaling**: All backgrounds scaled to fit screen
- **Fullscreen Mode**: `pygame.FULLSCREEN | pygame.NOFRAME`
- **Cross-Platform**: Works on various screen sizes

### Game States
- **START_MENU**: Main choice screen
- **TURTLE_PAGE**: Numerology realm
- **CRAB_PAGE**: Spiritual wisdom realm
- **RAT_PAGE**: Love and passion realm

## 🎨 Customization

### Adding New Fortunes
- **Turtle**: Edit `turtle_fortunes.py`
- **Crab**: Edit `fortunes.py`
- **Rat**: Edit `rat_fortunes.py`

### Voice Adjustments
- **Rate**: Speed of speech (`-r` parameter)
- **Pitch**: Voice tone (`-p` parameter)
- **Voice Type**: Different voice personalities (`-t` parameter)

### Background Images
- Replace `.jpg` files to change visual themes
- Images automatically scale to screen size
- Maintain aspect ratio for best results

## 🐛 Troubleshooting

### Audio Issues
- Check if `spd-say` is installed: `which spd-say`
- Verify audio devices: `aplay -l`
- Check volume levels: `amixer scontrols`

### Display Issues
- Ensure Pygame is properly installed
- Check screen resolution detection
- Verify image files exist and are readable

### Performance Issues
- Close unnecessary applications on Pi
- Ensure adequate power supply
- Check CPU/memory usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source. Feel free to use, modify, and distribute.

## 🙏 Acknowledgments

- **Artwork**: Beautiful background images for immersive experience
- **Pygame Community**: Excellent game development framework
- **Speech Dispatcher**: Reliable text-to-speech system
- **Raspberry Pi Foundation**: Amazing platform for creative projects

## 🚀 Future Enhancements

- [ ] Additional animal realms
- [ ] Music and sound effects
- [ ] Fortune history tracking
- [ ] Multi-language support
- [ ] Network multiplayer features
- [ ] Custom fortune creation interface

---

**🌟 May the wisdom of the Crab, Turtle, and Rat guide your path! 🌟** 