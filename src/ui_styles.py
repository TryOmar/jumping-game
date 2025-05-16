"""
UI Styles module for Jumping Ball Game.
Contains constants and definitions for consistent UI styling across screens.
"""

# Color definitions
COLORS = {
    # Background colors for different screens
    "BG_MAIN_MENU": (50, 100, 150),
    "BG_MAP_SELECTION": (70, 120, 170),
    "BG_OFFICIAL_MAPS": (60, 110, 160),
    "BG_SETTINGS": (60, 80, 140),
    "BG_HOW_TO_PLAY": (40, 90, 130),
    "BG_CUSTOM_MAPS": (50, 70, 120),
    "BG_GAME_OVER": (30, 30, 50),
    
    # UI element colors
    "BUTTON_BLUE": (40, 80, 120),
    "HIGHLIGHT_RED": (255, 0, 0),
    "TEXT_WHITE": (255, 255, 255),
    "TEXT_BLACK": (0, 0, 0),
    "SUCCESS_GREEN": (0, 255, 0),
    "WARNING_YELLOW": (255, 255, 0),
    "DANGER_RED": (255, 0, 0),
    
    # Platform colors
    "PLATFORM_REGULAR": (0, 255, 0),
    "PLATFORM_MOVING": (0, 0, 255),
    "PLATFORM_DISAPPEARING": (255, 255, 0),
    "PLATFORM_DANGEROUS": (255, 0, 0),
    
    # Additional UI colors
    "DESCRIPTION_TEXT": (220, 220, 220),
    "COMING_SOON_TEXT": (255, 220, 100),
    "OPTION_TEXT": (255, 255, 150),
    "SETTING_VALUE": (200, 255, 200),
}

# Font sizes
FONT_SIZES = {
    "TITLE_LARGE": 72,
    "TITLE_MEDIUM": 64,
    "HEADER": 56,
    "SUBHEADER": 48,
    "MENU_OPTION": 36,
    "STANDARD_TEXT": 32,
    "SMALL_TEXT": 24,
    "FOOTER_NOTE": 20,
}

# UI element dimensions
DIMENSIONS = {
    "BUTTON_WIDTH": 300,
    "BUTTON_HEIGHT": 100,
    "BUTTON_PADDING": 40,
    "OPTION_HEIGHT": 40,
    "SECTION_SPACING": 30,
    "BORDER_WIDTH": 3,
    "MAP_PREVIEW_SIZE": 120,
}

# Screen layout positions (percentage of screen height/width)
LAYOUT = {
    "TITLE_Y_PERCENT": 0.15,  # 15% from top
    "CONTENT_START_Y_PERCENT": 0.25,  # 25% from top
    "FOOTER_Y_PERCENT": 0.9,  # 90% from top (10% from bottom)
}

# Animation timing
ANIMATIONS = {
    "AUTO_JUMP_MSG_DURATION": 2000,  # milliseconds
    "COMING_SOON_FRAME_DURATION": 500,  # milliseconds
}

# Common UI creation functions
def create_centered_text(screen, text, font_size, color, y_pos):
    """Helper function to create centered text on the screen"""
    import pygame
    font = pygame.font.SysFont(None, font_size)
    rendered_text = font.render(text, True, color)
    screen_width = screen.get_width()
    screen.blit(rendered_text, (screen_width//2 - rendered_text.get_width()//2, y_pos))
    return rendered_text

def create_button(screen, text, rect, bg_color=COLORS["BUTTON_BLUE"], border_color=COLORS["TEXT_WHITE"], 
                 text_color=COLORS["TEXT_WHITE"], font_size=FONT_SIZES["MENU_OPTION"]):
    """Helper function to create a button with text"""
    import pygame
    # Draw button background
    pygame.draw.rect(screen, bg_color, rect)
    # Draw button border
    pygame.draw.rect(screen, border_color, rect, DIMENSIONS["BORDER_WIDTH"])
    
    # Draw button text
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, text_color)
    text_x = rect.centerx - text_surface.get_width() // 2
    text_y = rect.centery - text_surface.get_height() // 2
    screen.blit(text_surface, (text_x, text_y))
    
    return rect  # Return for click detection 