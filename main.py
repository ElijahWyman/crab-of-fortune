#!/usr/bin/env python3
"""
Crab of Fortune - Multi-Page Fortune Telling Experience
A mystical journey through different realms of wisdom and prophecy
"""

import pygame
import random
import time
from fortunes import FORTUNES
from turtle_fortunes import TURTLE_FORTUNES
from rat_fortunes import RAT_FORTUNES
from fortune_speaker import FortuneSpeaker

# Initialize Pygame
pygame.init()

# Window setup - Fullscreen for Raspberry Pi
try:
    # Try to get the actual screen resolution
    screen_info = pygame.display.Info()
    WINDOW_WIDTH = screen_info.current_w
    WINDOW_HEIGHT = screen_info.current_h
    print(f"✓ Detected screen resolution: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
except:
    # Fallback to common Pi resolution
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080
    print(f"⚠ Using fallback resolution: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)
pygame.display.set_caption("Crab of Fortune - Multi-Realms of Wisdom")
pygame.mouse.set_visible(False)  # Hide cursor for cleaner look

# Colors
TEXT_COLOR = (255, 255, 255)
POPUP_BG = (25, 25, 112, 200)
POPUP_BORDER = (70, 130, 180)

# Constants
PADDING = 20
FORTUNE_DISPLAY_TIME = 20  # Increased to 20 seconds

# Game states
class GameState:
    START_MENU = "start_menu"
    TURTLE_PAGE = "turtle_page"
    CRAB_PAGE = "crab_page"
    RAT_PAGE = "rat_page"

# Font setup
FONT_SIZE = int(WINDOW_HEIGHT * 0.06)
try:
    available_fonts = pygame.font.get_fonts()
    preferred_fonts = ['arial', 'helvetica', 'freesans', 'liberationsans', 'droidsans']
    
    chosen_font = None
    for font_name in preferred_fonts:
        if font_name in available_fonts:
            chosen_font = font_name
            break
    
    if chosen_font:
        fortune_font = pygame.font.SysFont(chosen_font, FONT_SIZE)
    else:
        fortune_font = pygame.font.Font(None, FONT_SIZE)
        
except Exception as e:
    print(f"Font initialization error: {e}")
    fortune_font = pygame.font.Font(None, FONT_SIZE)

# Load images with proper scaling
try:
    # Load and scale images to fit screen perfectly
    start_bg = pygame.image.load("START.jpg")
    start_bg = pygame.transform.scale(start_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    turtle_bg = pygame.image.load("turtle.jpg")
    turtle_bg = pygame.transform.scale(turtle_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    crab_bg = pygame.image.load("crab.jpg")
    crab_bg = pygame.transform.scale(crab_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    rat_bg = pygame.image.load("rat.jpg")
    rat_bg = pygame.transform.scale(rat_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    print(f"✓ Images loaded and scaled to {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    print(f"  - START.jpg: {start_bg.get_size()}")
    print(f"  - turtle.jpg: {turtle_bg.get_size()}")
    print(f"  - crab.jpg: {crab_bg.get_size()}")
    print(f"  - rat.jpg: {rat_bg.get_size()}")
    
except Exception as e:
    print(f"Error loading images: {e}")
    print("Creating fallback colored backgrounds...")
    
    # Create fallback colored backgrounds
    start_bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    start_bg.fill((25, 25, 112))  # Dark blue
    
    turtle_bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    turtle_bg.fill((34, 139, 34))  # Forest green
    
    crab_bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    crab_bg.fill((220, 20, 60))   # Crimson
    
    rat_bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    rat_bg.fill((128, 0, 128))    # Purple

# Button class for invisible click zones
class Button:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_hovered = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

# Initialize audio system
fortune_speaker = FortuneSpeaker()

# Game state
current_state = GameState.START_MENU
current_fortune = ""
fortune_popup_visible = False
popup_start_time = 0
countdown_start_time = 0
countdown_duration = 20  # 20 seconds

# Create invisible click zones for START menu
turtle_button = Button(
    WINDOW_WIDTH // 2 - 300,  # Left side
    WINDOW_HEIGHT // 2 - 100,  # Higher up to show more art
    250, 150                   # Larger size
)

crab_button = Button(
    WINDOW_WIDTH // 2 - 125,  # Center
    WINDOW_HEIGHT // 2 - 100,  # Higher up to show more art
    250, 150                   # Larger size
)

rat_button = Button(
    WINDOW_WIDTH // 2 + 50,   # Right side
    WINDOW_HEIGHT // 2 - 100,  # Higher up to show more art
    250, 150                   # Larger size
)

def get_random_fortune(fortune_type):
    """Get a random fortune based on the current page"""
    if fortune_type == GameState.TURTLE_PAGE:
        return random.choice(TURTLE_FORTUNES)
    elif fortune_type == GameState.CRAB_PAGE:
        return random.choice(FORTUNES)
    elif current_state == GameState.RAT_PAGE:
        return random.choice(RAT_FORTUNES)
    return "No fortune available."

def speak_current_fortune(fortune_text, voice_type="default"):
    """Speak the current fortune with the appropriate voice"""
    try:
        print(f"\n🎤 Speaking fortune with {voice_type} voice: {fortune_text}")
        print(f"🎤 Audio system status: {fortune_speaker.tts_engine}")
        success = fortune_speaker.speak_fortune(fortune_text, voice_type)
        if success:
            print("✓ Fortune spoken successfully")
        else:
            print("✗ Failed to speak fortune")
    except Exception as e:
        print(f"Error speaking fortune: {e}")
        import traceback
        traceback.print_exc()

def draw_fortune_popup(surface, fortune_text):
    """Draw the fortune popup with proper text wrapping"""
    if not fortune_popup_visible:
        return
        
    # Popup dimensions
    popup_width = int(WINDOW_WIDTH * 0.8)
    popup_height = int(WINDOW_HEIGHT * 0.6)
    popup_x = (WINDOW_WIDTH - popup_width) // 2
    popup_y = (WINDOW_HEIGHT - popup_height) // 2
    
    # Create semi-transparent surface
    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup_surface.fill(POPUP_BG)
    
    # Draw popup background
    surface.blit(popup_surface, (popup_x, popup_y))
    
    # Draw border
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    pygame.draw.rect(surface, POPUP_BORDER, popup_rect, 4, border_radius=15)
    
    # Split fortune into multiple lines with better word wrapping
    words = fortune_text.split()
    lines = []
    current_line = []
    current_width = 0
    max_width = popup_width - (PADDING * 4)

    for word in words:
        try:
            word_surface = fortune_font.render(word + " ", True, TEXT_COLOR)
            word_width = word_surface.get_width()
            
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width
        except Exception as e:
            print(f"Error rendering word '{word}': {e}")
            continue
    
    if current_line:
        lines.append(" ".join(current_line))
    
    # Calculate vertical spacing
    line_height = int(fortune_font.get_linesize() * 1.4)
    total_text_height = len(lines) * line_height
    start_y = popup_y + (popup_height - total_text_height) // 2
    
    # Draw each line
    for i, line in enumerate(lines):
        try:
            line_surface = fortune_font.render(line.strip(), True, TEXT_COLOR)
            line_rect = line_surface.get_rect()
            line_rect.centerx = WINDOW_WIDTH // 2
            line_rect.y = start_y + (i * line_height)
            surface.blit(line_surface, line_rect)
        except Exception as e:
            print(f"Error rendering line '{line}': {e}")
            continue

def draw_countdown_timer(surface):
    """Draw the countdown timer in the top-right corner"""
    if fortune_popup_visible:
        remaining_time = max(0, countdown_duration - int(time.time() - countdown_start_time))
        
        # Draw timer background
        timer_font = pygame.font.Font(None, 48)
        timer_text = f"Returning in {remaining_time}s"
        timer_surface = timer_font.render(timer_text, True, (255, 255, 255))
        timer_rect = timer_surface.get_rect()
        
        # Position in top-right corner
        timer_rect.topright = (WINDOW_WIDTH - 20, 20)
        
        # Draw semi-transparent background
        timer_bg = pygame.Surface((timer_rect.width + 20, timer_rect.height + 10), pygame.SRCALPHA)
        timer_bg.fill((0, 0, 0, 128))
        surface.blit(timer_bg, (timer_rect.x - 10, timer_rect.y - 5))
        
        # Draw timer text
        surface.blit(timer_surface, timer_rect)

def draw_current_page(surface):
    """Draw the current page based on game state"""
    if current_state == GameState.START_MENU:
        surface.blit(start_bg, (0, 0))
        # No text - just the beautiful art background
        
    elif current_state == GameState.TURTLE_PAGE:
        surface.blit(turtle_bg, (0, 0))
        draw_countdown_timer(surface)
        if fortune_popup_visible:
            draw_fortune_popup(surface, current_fortune)
            
    elif current_state == GameState.CRAB_PAGE:
        surface.blit(crab_bg, (0, 0))
        draw_countdown_timer(surface)
        if fortune_popup_visible:
            draw_fortune_popup(surface, current_fortune)
            
    elif current_state == GameState.RAT_PAGE:
        surface.blit(rat_bg, (0, 0))
        draw_countdown_timer(surface)
        if fortune_popup_visible:
            draw_fortune_popup(surface, current_fortune)

def show_fortune_and_speak():
    """Show fortune and speak it immediately with the appropriate voice"""
    global current_fortune, fortune_popup_visible, popup_start_time, countdown_start_time
    
    current_fortune = get_random_fortune(current_state)
    fortune_popup_visible = True
    popup_start_time = time.time()
    countdown_start_time = time.time()
    
    # Determine voice type based on current state
    if current_state == GameState.TURTLE_PAGE:
        voice_type = "turtle"  # Slow, wise, deep voice
    elif current_state == GameState.CRAB_PAGE:
        voice_type = "crab"    # Mystical, medium pace, male voice
    elif current_state == GameState.RAT_PAGE:
        voice_type = "rat"     # Passionate, comfortable pace, female voice
    else:
        voice_type = "default"
    
    # Speak the fortune immediately with the appropriate voice!
    print(f"🎤 Auto-speaking fortune for {current_state} with {voice_type} voice: {current_fortune[:50]}...")
    speak_current_fortune(current_fortune, voice_type)

def update_timers():
    """Update timers and return to start menu when time is up"""
    global fortune_popup_visible, current_state
    
    if fortune_popup_visible and time.time() - popup_start_time > FORTUNE_DISPLAY_TIME:
        fortune_popup_visible = False
        current_state = GameState.START_MENU

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    current_time = time.time()
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Handle escape key to exit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break
                
        # Handle button events based on current state
        if current_state == GameState.START_MENU:
            if turtle_button.handle_event(event):
                current_state = GameState.TURTLE_PAGE
                show_fortune_and_speak()
            elif crab_button.handle_event(event):
                current_state = GameState.CRAB_PAGE
                show_fortune_and_speak()
            elif rat_button.handle_event(event):
                current_state = GameState.RAT_PAGE
                show_fortune_and_speak()
    
    # Update game state
    update_timers()
    
    # Draw everything
    draw_current_page(screen)
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit() 