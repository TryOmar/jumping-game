import pygame
import sys
from src.constants import WHITE, BLACK
from src.game_state import GameState, StateManager
from src.player import Player
from src.map import Map

class Game:
    def __init__(self, width=800, height=600, fps=60):
        # Game window settings
        self.width = width
        self.height = height
        self.fps = fps
        
        # Setup game window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Jumping Ball Game")
        self.clock = pygame.time.Clock()
        
        # Initialize state management
        self.state_manager = StateManager()
        
        # Initialize game objects (will be created properly when starting game)
        self.player = None
        self.current_map = None
        self.camera_y = 0
        
        # Game state
        self.running = True
        
    def handle_events(self):
        """Process all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Process keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Escape behaves differently based on state
                    if self.state_manager.is_state(GameState.PLAYING):
                        self.state_manager.change_state(GameState.PAUSED)
                    elif self.state_manager.is_state(GameState.PAUSED):
                        self.state_manager.change_state(GameState.PLAYING)
                    elif self.state_manager.is_state(GameState.MAIN_MENU):
                        self.running = False
                    else:
                        self.state_manager.return_to_previous()
                
                # Temporary state change keys for testing
                if event.key == pygame.K_1:
                    self.state_manager.change_state(GameState.MAIN_MENU)
                elif event.key == pygame.K_2:
                    self.state_manager.change_state(GameState.PLAYING)
                    if not self.player:
                        # Create player and map when entering play state
                        self.player = Player(self.width // 2, self.height - 100)
                        self.current_map = Map()
                elif event.key == pygame.K_3:
                    self.state_manager.change_state(GameState.GAME_OVER, score=100)
    
    def update(self):
        """Update game state"""
        if self.state_manager.is_state(GameState.PLAYING):
            # Only update game objects when in PLAYING state
            if self.player and self.current_map:
                self.player.update()
                self.current_map.update(self.camera_y)
                
                # Check collisions
                # self.current_map.check_collision(self.player)
                
                # Check if player has reached target height
                # if self.camera_y <= self.current_map.target_height:
                #     self.state_manager.change_state(GameState.GAME_OVER, 
                #                                     score=abs(int(self.camera_y)), 
                #                                     reason="Victory")
    
    def render(self):
        """Draw everything to the screen"""
        # Clear the screen
        self.screen.fill(WHITE)
        
        # Render based on game state
        if self.state_manager.is_state(GameState.MAIN_MENU):
            self._render_main_menu()
        elif self.state_manager.is_state(GameState.MAP_SELECT):
            self._render_map_select()
        elif self.state_manager.is_state(GameState.PLAYING):
            self._render_game()
        elif self.state_manager.is_state(GameState.PAUSED):
            self._render_game()  # Render game in background
            self._render_pause_menu()
        elif self.state_manager.is_state(GameState.GAME_OVER):
            self._render_game_over()
        elif self.state_manager.is_state(GameState.SETTINGS):
            self._render_settings()
        elif self.state_manager.is_state(GameState.HOW_TO_PLAY):
            self._render_how_to_play()
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Process input
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Render new frame
            self.render()
            
            # Control the game speed
            self.clock.tick(self.fps)
        
        # Clean up
        pygame.quit()
        sys.exit()
    
    # Helper methods for rendering different states
    
    def _render_main_menu(self):
        """Render the main menu screen"""
        # Temp rectangle to show it's the main menu
        pygame.draw.rect(self.screen, BLACK, (self.width//2 - 100, self.height//2 - 100, 200, 200))
        
        # Render text (will be improved later)
        font = pygame.font.SysFont(None, 48)
        text = font.render("MAIN MENU", True, WHITE)
        self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - text.get_height()//2))
        
        # Instructions
        font_small = pygame.font.SysFont(None, 24)
        text = font_small.render("Press 2 to start game, ESC to exit", True, WHITE)
        self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2 + 50))
    
    def _render_map_select(self):
        """Render the map selection screen"""
        # Will be implemented later
        pass
    
    def _render_game(self):
        """Render the actual gameplay"""
        # Draw map
        if self.current_map:
            self.current_map.draw(self.screen, self.camera_y)
        
        # Draw player
        if self.player:
            self.player.draw(self.screen)
        
        # Draw score
        font = pygame.font.SysFont(None, 36)
        score = self.state_manager.get_state_data("score")
        text = font.render(f"Score: {score}", True, BLACK)
        self.screen.blit(text, (10, 10))
    
    def _render_pause_menu(self):
        """Render pause menu overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% transparency
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        font = pygame.font.SysFont(None, 48)
        text = font.render("PAUSED", True, WHITE)
        self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - text.get_height()//2))
        
        # Instructions
        font_small = pygame.font.SysFont(None, 24)
        text = font_small.render("Press ESC to resume, 1 for main menu", True, WHITE)
        self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2 + 50))
    
    def _render_game_over(self):
        """Render game over screen"""
        # Game over text
        font = pygame.font.SysFont(None, 64)
        text = font.render("GAME OVER", True, BLACK)
        self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - 100))
        
        # Score
        score = self.state_manager.get_state_data("score")
        font = pygame.font.SysFont(None, 48)
        text = font.render(f"Score: {score}", True, BLACK)
        self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2))
        
        # Instructions
        font_small = pygame.font.SysFont(None, 24)
        text = font_small.render("Press 1 to return to main menu", True, BLACK)
        self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2 + 100))
    
    def _render_settings(self):
        """Render settings screen"""
        # Will be implemented later
        pass
    
    def _render_how_to_play(self):
        """Render instructions screen"""
        # Will be implemented later
        pass 