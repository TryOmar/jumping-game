import pygame
from src.constants import WHITE
from src.game_state import GameState

class BaseRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
    
    def render(self, game):
        """Draw everything to the screen"""
        # Clear the screen
        self.screen.fill(WHITE)
        
        # Delegate rendering to specialized renderers based on game state
        from src.renderers.menu_renderer import MenuRenderer
        from src.renderers.gameplay_renderer import GameplayRenderer
        from src.renderers.ui_renderer import UIRenderer
        
        menu_renderer = MenuRenderer(self.screen)
        gameplay_renderer = GameplayRenderer(self.screen)
        ui_renderer = UIRenderer(self.screen)
        
        # Render based on game state
        if game.state_manager.is_state(GameState.MAIN_MENU):
            menu_renderer.render_main_menu(game)
        elif game.state_manager.is_state(GameState.MAP_SELECT):
            menu_renderer.render_map_select(game)
        elif game.state_manager.is_state(GameState.PLAYING):
            gameplay_renderer.render_game(game)
        elif game.state_manager.is_state(GameState.PAUSED):
            gameplay_renderer.render_game(game)  # Render game in background
            gameplay_renderer.render_pause_menu(game)
        elif game.state_manager.is_state(GameState.GAME_OVER):
            ui_renderer.render_game_over(game)
        elif game.state_manager.is_state(GameState.SETTINGS):
            ui_renderer.render_settings(game)
        elif game.state_manager.is_state(GameState.HOW_TO_PLAY):
            ui_renderer.render_how_to_play(game)
        
        # Update the display
        pygame.display.flip() 