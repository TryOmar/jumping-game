import pygame
from src.constants import WHITE, BLACK
from src.ui_styles import COLORS, FONT_SIZES, DIMENSIONS, create_centered_text

class MainMenuRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
    
    def render(self, game):
        """Render the main menu screen"""
        # Draw background
        self.screen.fill(COLORS["BG_MAIN_MENU"])
        
        # Draw game title
        title_font = pygame.font.SysFont(None, FONT_SIZES["TITLE_LARGE"])
        title_text = title_font.render("JUMPING BALL", True, COLORS["TEXT_WHITE"])
        self.screen.blit(title_text, (self.width//2 - title_text.get_width()//2, 100))
        
        # Draw decorative circles
        pygame.draw.circle(self.screen, COLORS["TEXT_BLACK"], (self.width//2, 200), 30)
        pygame.draw.circle(self.screen, (200, 200, 0), (self.width//2 - 80, 220), 15)
        pygame.draw.circle(self.screen, (0, 200, 200), (self.width//2 + 80, 220), 15)
        
        # Draw menu options
        option_height = DIMENSIONS["OPTION_HEIGHT"]
        start_y = self.height // 2
        
        game.menu_option_rects = [] # Initialize the list to store rects

        for i, option in enumerate(game.menu_options):
            # Determine if this option is selected
            is_selected = (i == game.selected_option)
            
            # Choose font color based on selection
            color = COLORS["TEXT_BLACK"] if not is_selected else COLORS["HIGHLIGHT_RED"]
            
            # Create option text
            option_font = pygame.font.SysFont(None, FONT_SIZES["MENU_OPTION"])
            option_text = option_font.render(option, True, color)
            
            # Draw option text
            option_y = start_y + i * option_height
            option_x = self.width//2 - option_text.get_width()//2
            self.screen.blit(option_text, (option_x, option_y))
            
            # Store the rectangle for click detection
            option_rect = option_text.get_rect(topleft=(option_x, option_y))
            game.menu_option_rects.append(option_rect)

            # Draw indicator if selected
            if is_selected:
                # Draw arrow or highlight
                pygame.draw.polygon(self.screen, COLORS["HIGHLIGHT_RED"], [
                    (option_x - 20, option_y + option_text.get_height()//2),
                    (option_x - 10, option_y + option_text.get_height()//2 - 5),
                    (option_x - 10, option_y + option_text.get_height()//2 + 5),
                ])
        
        # Draw footer text using helper function
        create_centered_text(
            self.screen,
            "Use arrow keys to select, Enter to confirm",
            FONT_SIZES["FOOTER_NOTE"],
            COLORS["TEXT_WHITE"],
            self.height - 50
        ) 