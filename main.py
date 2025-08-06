import pygame
import random
import sys
import os
import time
from pygame import mixer
from fortunes import FORTUNES

# Configuration
FORTUNE_DISPLAY_TIME = 10  # seconds to display the fortune
BUTTON_REAPPEAR_DELAY = 1  # seconds to wait after fortune disappears before showing button

# Disable on-screen keyboard and touch events
os.environ['SDL_NOMOUSE'] = '1'
os.environ['DISPLAY'] = ':0.0'
os.environ['SDL_KMSDRM_REQUIRE_DRM'] = '0'
os.environ['SDL_VIDEO_ALLOW_SCREENSAVER'] = '1'

# Initialize Pygame
pygame.init()
mixer.init()

# Check if running on Raspberry Pi
is_raspberry_pi = os.uname()[4].startswith('arm') or os.uname()[4].startswith('aarch')

# Get the current screen resolution
screen_info = pygame.display.Info()
WINDOW_WIDTH = screen_info.current_w
WINDOW_HEIGHT = screen_info.current_h
FPS = 30 if is_raspberry_pi else 60  # Lower FPS for Pi

# Colors
SAND_COLOR = (238, 214, 175)
OCEAN_BLUE = (65, 105, 225)
CRAB_RED = (255, 64, 64)
TEXT_COLOR = (44, 62, 80)
BUTTON_COLOR = (0, 0, 0)  # Black button
BUTTON_HOVER_COLOR = (40, 40, 40)  # Dark gray on hover

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)
pygame.display.set_caption("Crab of Fortune")
pygame.mouse.set_visible(False)  # Hide the cursor
clock = pygame.time.Clock()

# Load and scale the start image
start_image = pygame.image.load('START.jpg')
start_image = pygame.transform.scale(start_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Font setup with fallback system
def init_fonts():
    fortune_size = int(WINDOW_HEIGHT * 0.045)  # Slightly smaller size for better rendering
    
    # Try loading the custom font
    try:
        if os.path.exists('PressStart2P-Regular.ttf'):
            custom_font = pygame.font.Font('PressStart2P-Regular.ttf', fortune_size)
            # Test render to ensure font works
            test = custom_font.render("Test", True, (0, 0, 0))
            if test:
                return custom_font
    except Exception as e:
        print(f"Custom font loading failed: {e}")
    
    # First fallback: Try Arial or a similar common font
    try:
        return pygame.font.SysFont('arial', fortune_size)
    except Exception as e:
        print(f"Arial font loading failed: {e}")
    
    # Final fallback: Use default Pygame font
    try:
        return pygame.font.Font(None, fortune_size)
    except Exception as e:
        print(f"Default font loading failed: {e}")
        sys.exit(1)

# Initialize the font
fortune_font = init_fonts()

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        self.color = BUTTON_COLOR
        self.visible = True
        
    def draw(self, surface):
        if not self.visible:
            return
            
        # Don't draw anything - button is completely transparent
        # But keep the clickable area active
        pass
        
    def handle_event(self, event):
        if not self.visible:
            return False
            
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

# Create fortune button in lower right with adjusted size
original_width = int(WINDOW_WIDTH * 0.375)  # Original width (37.5% of screen)
button_width = int(original_width * 0.7)  # Reduce width by 30%
button_height = int(WINDOW_HEIGHT * 0.125)  # 12.5% of screen height
fortune_button = Button(
    WINDOW_WIDTH - button_width - int(WINDOW_WIDTH * 0.05),  # 5% from right edge
    WINDOW_HEIGHT - button_height - int(WINDOW_HEIGHT * 0.05) - 70,  # Move up 70px total
    button_width,
    button_height,
    "Tell My Fortune!"
)

def draw_fortune_popup(surface, fortune_text):
    global fortune_font
    
    # Calculate popup dimensions
    PADDING = 10  # 10px padding from screen edges
    popup_height = (WINDOW_HEIGHT // 2) + 20  # 50% of screen height plus 20px
    popup_width = WINDOW_WIDTH - (PADDING * 2)  # Full width minus padding
    popup_y = WINDOW_HEIGHT - popup_height - PADDING  # Position at bottom with padding

    # Create popup background
    popup_rect = pygame.Rect(PADDING, popup_y, popup_width, popup_height)
    pygame.draw.rect(surface, (255, 255, 255), popup_rect, border_radius=10)  # White background
    pygame.draw.rect(surface, OCEAN_BLUE, popup_rect, 3, border_radius=10)    # Blue border

    # Split fortune into multiple lines
    words = fortune_text.split()
    lines = []
    current_line = []
    current_width = 0
    max_width = popup_width - (PADDING * 6)  # Increased padding for larger text

    # Try to render text, reinitialize font if needed
    def try_render(text):
        global fortune_font
        try:
            return fortune_font.render(text, True, TEXT_COLOR)
        except pygame.error:
            fortune_font = init_fonts()
            return fortune_font.render(text, True, TEXT_COLOR)

    for word in words:
        word_surface = try_render(word + " ")
        word_width = word_surface.get_width()
        
        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_width = word_width
    
    if current_line:
        lines.append(" ".join(current_line))

    # Calculate vertical spacing
    line_height = int(fortune_font.get_linesize() * 1.2)  # Add 20% more space between lines
    total_text_height = len(lines) * line_height
    start_y = popup_y + (popup_height - total_text_height) // 2  # Center text vertically in popup

    # Draw each line
    for i, line in enumerate(lines):
        line_surface = try_render(line.strip())
        line_rect = line_surface.get_rect()
        line_rect.centerx = WINDOW_WIDTH // 2
        line_rect.y = start_y + (i * line_height)
        surface.blit(line_surface, line_rect)

def main():
    current_fortune = ""
    show_fortune = False
    fortune_start_time = 0
    
    running = True
    while running:
        current_time = time.time()
        
        # Check if fortune should be hidden
        if show_fortune and current_time - fortune_start_time >= FORTUNE_DISPLAY_TIME:
            show_fortune = False
            # Wait a moment before showing the button again
            time.sleep(BUTTON_REAPPEAR_DELAY)
            fortune_button.visible = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # Allow escape key to exit
                
            if fortune_button.handle_event(event):
                current_fortune = random.choice(FORTUNES)
                show_fortune = True
                fortune_start_time = current_time
                fortune_button.visible = False  # Hide button when fortune is shown
        
        # Draw background image
        screen.blit(start_image, (0, 0))
        
        # Draw fortune popup if active
        if show_fortune:
            draw_fortune_popup(screen, current_fortune)
        
        # Draw fortune button
        fortune_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 