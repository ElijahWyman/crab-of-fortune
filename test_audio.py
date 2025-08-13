#!/usr/bin/env python3
"""
Test script for the audio system
Run this to verify text-to-speech is working before running the main game
"""

from fortune_speaker import FortuneSpeaker
import time

def main():
    print("🎤 Testing Crab of Fortune Audio System")
    print("=" * 50)
    
    try:
        # Initialize the audio system
        print("Initializing audio system...")
        speaker = FortuneSpeaker()
        
        # Test the audio system
        print("\nTesting audio output...")
        success = speaker.test_audio()
        
        if success:
            print("\n✅ Audio test successful! The system is ready to speak fortunes.")
            print("You can now run the main game with: python3 main.py")
        else:
            print("\n❌ Audio test failed. Please check your audio setup.")
            
    except Exception as e:
        print(f"\n❌ Error during audio test: {e}")
        print("Please check your audio system configuration.")
    
    print("\n" + "=" * 50)
    print("Audio test complete.")

if __name__ == "__main__":
    main()
