import pygame
from src.constants import WHITE
from src.game_state import GameState

class BaseRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Initialize all renderers
        self.init_renderers()
    
    def init_renderers(self):
        """Initialize or reinitialize all renderers"""
        # Update width and height
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        # Import renderers
        from src.renderers.main_menu_renderer import MainMenuRenderer
        from src.renderers.map_selection_renderer import MapSelectionRenderer
        from src.renderers.gameplay_renderer import GameplayRenderer
        from src.renderers.game_over_renderer import GameOverRenderer
        from src.renderers.settings_renderer import SettingsRenderer
        from src.renderers.how_to_play_renderer import HowToPlayRenderer
        
        # Initialize all renderers with the current screen
        self.main_menu_renderer = MainMenuRenderer(self.screen)
        self.map_selection_renderer = MapSelectionRenderer(self.screen)
        self.gameplay_renderer = GameplayRenderer(self.screen)
        self.game_over_renderer = GameOverRenderer(self.screen)
        self.settings_renderer = SettingsRenderer(self.screen)
        self.how_to_play_renderer = HowToPlayRenderer(self.screen)
    
    def render(self, game):
        """Draw everything to the screen"""
        # Clear the screen
        self.screen.fill(WHITE)
        
        # Render based on game state
        if game.state_manager.is_state(GameState.MAIN_MENU):
            self.main_menu_renderer.render(game)
        elif game.state_manager.is_state(GameState.MAP_SELECT):
            self.map_selection_renderer.render_map_type_selection(game)
        elif game.state_manager.is_state(GameState.OFFICIAL_MAPS):
            self.map_selection_renderer.render_official_maps(game)
        elif game.state_manager.is_state(GameState.CUSTOM_MAPS):
            self.map_selection_renderer.render_custom_maps(game)
        elif game.state_manager.is_state(GameState.PLAYING):
            self.gameplay_renderer.render_game(game)
        elif game.state_manager.is_state(GameState.PAUSED):
            self.gameplay_renderer.render_game(game)  # Render game in background
            self.gameplay_renderer.render_pause_menu(game)
        elif game.state_manager.is_state(GameState.GAME_OVER):
            self.game_over_renderer.render(game)
        elif game.state_manager.is_state(GameState.SETTINGS):
            self.settings_renderer.render(game)
        elif game.state_manager.is_state(GameState.HOW_TO_PLAY):
            self.how_to_play_renderer.render(game)
        
        # Update the display
        pygame.display.flip() 