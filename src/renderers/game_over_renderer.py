import pygame
from src.constants import WHITE, BLACK, RED, GREEN
from src.ui_styles import COLORS, FONT_SIZES, DIMENSIONS, create_centered_text, create_button

class GameOverRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.selected_option = 0  # Default to "Try Again"
        
    def render(self, game):
        """Render the game over screen"""
        # Draw background
        self.screen.fill(COLORS["BG_GAME_OVER"])
        
        # Get game over info
        score = game.state_manager.get_state_data("score") or 0
        reason = game.state_manager.get_state_data("reason") or "Fall"
        
        # Draw game over text
        if reason == "Victory":
            main_color = COLORS["SUCCESS_GREEN"]
            title_text = "LEVEL COMPLETE!"
        else:
            main_color = COLORS["DANGER_RED"]
            title_text = "GAME OVER"
        
        # Draw title
        title_font = pygame.font.SysFont(None, FONT_SIZES["TITLE_MEDIUM"])
        title_rendered = title_font.render(title_text, True, main_color)
        self.screen.blit(title_rendered, (self.width//2 - title_rendered.get_width()//2, 120))
        
        # Draw reason if not victory
        if reason != "Victory":
            create_centered_text(
                self.screen,
                f"Reason: {reason}",
                FONT_SIZES["MENU_OPTION"],
                COLORS["TEXT_WHITE"],
                200
            )
        
        # Draw decorative line
        pygame.draw.rect(self.screen, main_color, (self.width//2 - 150, 250, 300, 3))
        
        # Draw score
        create_centered_text(
            self.screen,
            f"Score: {score}",
            FONT_SIZES["SUBHEADER"],
            COLORS["TEXT_WHITE"],
            280
        )
        
        # Draw high score
        create_centered_text(
            self.screen,
            f"High Score: {score}",  # For now, just use current score
            FONT_SIZES["STANDARD_TEXT"],
            COLORS["COMING_SOON_TEXT"],
            330
        )
        
        # Store option selection in game state if not already there
        if not hasattr(game, 'game_over_selected_option'):
            game.game_over_selected_option = 0
        
        # Use the stored selection
        self.selected_option = game.game_over_selected_option
        
        # Draw options
        options = ["Try Again", "Main Menu"]
        option_y = 420
        option_spacing = 50
        
        for i, option in enumerate(options):
            y_pos = option_y + i * option_spacing
            
            # Determine if selected
            color = COLORS["TEXT_WHITE"] if i != self.selected_option else main_color
            
            option_text = create_centered_text(
                self.screen,
                option,
                FONT_SIZES["MENU_OPTION"],
                color,
                y_pos
            )
            
            # Draw indicator if selected
            if i == self.selected_option:
                # Get the x position where the text was rendered
                text_x = self.width//2 - option_text.get_width()//2
                pygame.draw.circle(
                    self.screen, 
                    main_color, 
                    (text_x - 20, y_pos + option_text.get_height()//2), 
                    8
                )
        
        # Instructions
        create_centered_text(
            self.screen,
            "Use UP/DOWN to select, ENTER to confirm, or ESC for main menu",
            FONT_SIZES["FOOTER_NOTE"],
            COLORS["TEXT_WHITE"],
            self.height - 40
        )
        
        # Store button rectangles for click detection
        option_font = pygame.font.SysFont(None, FONT_SIZES["MENU_OPTION"])
        button_rects = []
        
        for i, option in enumerate(options):
            y_pos = option_y + i * option_spacing
            option_text = option_font.render(option, True, COLORS["TEXT_WHITE"])
            text_width = option_text.get_width()
            text_height = option_text.get_height()
            
            # Create a slightly larger clickable area
            button_rect = pygame.Rect(
                self.width//2 - text_width//2 - 30,  # Extra space for the indicator
                y_pos - 5,  # Slight padding above
                text_width + 60,  # Extra width for better clickability
                text_height + 10  # Extra height for better clickability
            )
            button_rects.append(button_rect)
        
        # Store the rects in the game object for click detection
        game.game_over_buttons = button_rects 