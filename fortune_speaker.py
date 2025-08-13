"""
Fortune Speaker Module
Handles speaking fortunes aloud using text-to-speech
"""

import os
import subprocess
import tempfile
import time

def run_system_command(cmd, verbose=True):
    """Run a system command and return output"""
    try:
        if verbose:
            print(f"\nExecuting command: {cmd}")
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if verbose:
            print(f"STDOUT: {result.stdout}")
            if result.stderr:
                print(f"STDERR: {result.stderr}")
            print(f"Exit code: {result.returncode}")
        
        return result.stdout, result.returncode
    except Exception as e:
        if verbose:
            print(f"Command failed: {e}")
        return None, -1

class FortuneSpeaker:
    def __init__(self):
        """Initialize the text-to-speech system"""
        print("\n=== Audio System Initialization ===")
        print("Initializing text-to-speech for Crab of Fortune")
        
        # Check for available text-to-speech engines
        stdout, exit_code = run_system_command("which spd-say")
        if exit_code == 0:
            self.tts_engine = "spd-say"
            print("✓ spd-say found - will use for text-to-speech")
        else:
            stdout, exit_code = run_system_command("which espeak")
            if exit_code == 0:
                self.tts_engine = "espeak"
                print("✓ espeak found - will use for text-to-speech")
            else:
                stdout, exit_code = run_system_command("which festival")
                if exit_code == 0:
                    self.tts_engine = "festival"
                    print("✓ festival found - will use for text-to-speech")
                else:
                    print("No text-to-speech engine found, audio will be disabled")
                    self.tts_engine = None
        
        # Check audio system
        print("\nChecking audio system:")
        run_system_command("aplay -l")
        run_system_command("amixer scontrols")
        
        # Set volume to a reasonable level
        print("\nSetting audio volume:")
        run_system_command("amixer set Master 70%")
        run_system_command("amixer set PCM 70%")

    def speak_fortune(self, fortune_text, voice_type="default"):
        """Speak the fortune text aloud with different voices for each animal"""
        try:
            print(f"\n🎤 Speaking fortune with {voice_type} voice: {fortune_text}")
            
            if not self.tts_engine:
                print("✗ No text-to-speech engine available")
                return False
            
            if self.tts_engine == "spd-say":
                # Use spd-say with different voice settings for each animal
                if voice_type == "turtle":
                    # Turtle: Slow, wise, deep voice
                    cmd = f'spd-say -r -50 -p -20 -t female3 "{fortune_text}"'
                elif voice_type == "crab":
                    # Crab: Mystical, medium pace, male voice
                    cmd = f'spd-say -r -30 -p 0 -t male1 "{fortune_text}"'
                elif voice_type == "rat":
                    # Rat: Passionate, female voice (slowed down)
                    cmd = f'spd-say -r -20 -p 20 -t female2 "{fortune_text}"'
                else:
                    # Default voice
                    cmd = f'spd-say "{fortune_text}"'
                
                stdout, exit_code = run_system_command(cmd, verbose=False)
                
                if exit_code == 0:
                    print(f"✓ Fortune spoken successfully with spd-say ({voice_type} voice)")
                    return True
                else:
                    print(f"✗ Failed to speak fortune with spd-say ({voice_type} voice)")
                    return False
                    
            elif self.tts_engine == "espeak":
                # Use espeak with different voice settings for each animal
                if voice_type == "turtle":
                    # Turtle: Slow, wise, deep voice
                    cmd = f'espeak -v en-us+m3 -s 120 -p 30 -a 100 "{fortune_text}"'
                elif voice_type == "crab":
                    # Crab: Mystical, medium pace, male voice
                    cmd = f'espeak -v en-us+m2 -s 150 -p 50 -a 80 "{fortune_text}"'
                elif voice_type == "rat":
                    # Rat: Passionate, female voice (slowed down)
                    cmd = f'espeak -v en-us+f2 -s 140 -p 70 -a 120 "{fortune_text}"'
                else:
                    # Default voice
                    cmd = f'espeak -v en-us+f3 -s 150 -p 50 "{fortune_text}"'
                
                stdout, exit_code = run_system_command(cmd, verbose=False)
                
                if exit_code == 0:
                    print(f"✓ Fortune spoken successfully with espeak ({voice_type} voice)")
                    return True
                else:
                    print(f"✗ Failed to speak fortune with espeak ({voice_type} voice)")
                    return False
                    
            elif self.tts_engine == "festival":
                # Use festival as fallback (limited voice control)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
                temp_file.write(fortune_text.encode())
                temp_file.close()
                
                cmd = f'festival --tts {temp_file.name}'
                stdout, exit_code = run_system_command(cmd, verbose=False)
                
                # Clean up temp file
                os.unlink(temp_file.name)
                
                if exit_code == 0:
                    print(f"✓ Fortune spoken successfully with festival ({voice_type} voice)")
                    return True
                else:
                    print(f"✗ Failed to speak fortune with festival ({voice_type} voice)")
                    return False
            
        except Exception as e:
            print(f"Error speaking fortune: {e}")
            return False

    def test_audio(self):
        """Test the audio system with a simple message"""
        print("\n🔊 Testing audio system...")
        test_message = "Audio test successful. Crab of Fortune is ready to speak your fortune."
        return self.speak_fortune(test_message)

    def stop_audio(self):
        """Stop any currently playing audio"""
        try:
            # Kill any running espeak processes
            run_system_command("pkill -f espeak", verbose=False)
            # Kill any running festival processes
            run_system_command("pkill -f festival", verbose=False)
            print("✓ Audio stopped")
        except Exception as e:
            print(f"Error stopping audio: {e}")
