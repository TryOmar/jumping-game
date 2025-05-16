import pygame
from src.constants import WHITE, BLACK, RED, GREEN
from src.ui_styles import COLORS, FONT_SIZES, DIMENSIONS, create_centered_text, create_button

class GameOverRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        # self.selected_option = 0 # This will be driven by game.game_over_selected_option
        
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
        
        # Draw high score (Placeholder)
        # TODO: Implement actual high score loading/saving
        create_centered_text(
            self.screen,
            f"High Score: {score}",  # For now, just use current score as placeholder
            FONT_SIZES["STANDARD_TEXT"],
            COLORS["COMING_SOON_TEXT"],
            330
        )
        
        # Define button data (label and action) - THIS IS CRITICAL
        buttons_data = [
            {"label": "Try Again", "action": "retry"},
            {"label": "Main Menu", "action": "main_menu"}
        ]
        game.game_over_buttons = buttons_data # Store the data list

        # Store option selection in game state if not already there
        if not hasattr(game, 'game_over_selected_option'):
            game.game_over_selected_option = 0 # Default to "Try Again"
        
        # Current selected option index
        current_selected_option_index = game.game_over_selected_option
        
        # Draw options and create button rects
        option_y_start = 400 # Start Y position for the first button
        option_spacing = 60  # Vertical spacing between buttons
        
        game.game_over_button_rects = [] # Initialize list for actual pygame.Rects

        option_font = pygame.font.SysFont(None, FONT_SIZES["MENU_OPTION"])

        for i, button_info in enumerate(game.game_over_buttons):
            option_label = button_info["label"]
            y_pos = option_y_start + i * option_spacing
            
            is_selected = (i == current_selected_option_index)
            text_color = COLORS["HIGHLIGHT_RED"] if is_selected else COLORS["TEXT_WHITE"]
            
            # Render the text to get its dimensions
            rendered_text_surface = option_font.render(option_label, True, text_color)
            text_width = rendered_text_surface.get_width()
            text_height = rendered_text_surface.get_height()
            
            # Calculate position for centered text
            text_x = self.width // 2 - text_width // 2
            self.screen.blit(rendered_text_surface, (text_x, y_pos))
            
            # Create and store button rect based on the rendered text
            # Make it slightly larger for easier clicking
            button_rect_padding_x = 30 
            button_rect_padding_y = 10
            button_rect = pygame.Rect(
                text_x - button_rect_padding_x // 2,
                y_pos - button_rect_padding_y // 2,
                text_width + button_rect_padding_x,
                text_height + button_rect_padding_y
            )
            game.game_over_button_rects.append(button_rect)

            # Draw indicator if selected
            if is_selected:
                indicator_x = text_x - 20 # To the left of the text
                indicator_y = y_pos + text_height // 2
                pygame.draw.circle(
                    self.screen, 
                    COLORS["HIGHLIGHT_RED"], # Use the highlight color for the indicator
                    (indicator_x, indicator_y), 
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