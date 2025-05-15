import pygame
import sys
from src.constants import WHITE, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT
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
        
        # Debug mode
        self.debug_mode = False
        
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
                
                # Toggle debug mode with F1
                if event.key == pygame.K_F1:
                    self.debug_mode = not self.debug_mode
                
                # Temporary state change keys for testing
                if event.key == pygame.K_1:
                    self.state_manager.change_state(GameState.MAIN_MENU)
                elif event.key == pygame.K_2:
                    self.state_manager.change_state(GameState.PLAYING)
                    if not self.player:
                        # Create player and map when entering play state
                        self.init_game()
                elif event.key == pygame.K_3:
                    self.state_manager.change_state(GameState.GAME_OVER, score=100)
    
    def init_game(self):
        """Initialize game objects for a new game"""
        self.player = Player(self.width // 2, self.height - 100)
        self.current_map = Map()
        self.current_map.generate_map()  # Generate initial platforms
        self.camera_y = 0
        self.state_manager.set_state_data("score", 0)
    
    def update(self):
        """Update game state"""
        if self.state_manager.is_state(GameState.PLAYING):
            # Only update game objects when in PLAYING state
            if self.player and self.current_map:
                # Handle player input
                keys = pygame.key.get_pressed()
                self.player.handle_input(keys)
                
                # Update player
                self.player.update()
                
                # Check if player is going off screen horizontally (wrap around)
                if self.player.x < 0:
                    self.player.x = self.width
                elif self.player.x > self.width:
                    self.player.x = 0
                
                # Update camera position if player gets too high
                if self.player.y < self.height // 3:
                    # Move camera up, move player down relatively
                    camera_shift = self.height // 3 - self.player.y
                    self.camera_y -= camera_shift
                    self.player.y += camera_shift
                    # Update score based on height
                    self.state_manager.set_state_data("score", abs(int(self.camera_y)))
                
                # Check if player has fallen off the bottom
                if self.player.y > self.height:
                    self.state_manager.change_state(GameState.GAME_OVER, 
                                                 score=abs(int(self.camera_y)), 
                                                 reason="Fall")
                
                # Update map and check collisions
                self.current_map.update(self.camera_y)
                self.check_platform_collisions()
                
                # Check if player has reached target height
                if self.camera_y <= self.current_map.target_height:
                    self.state_manager.change_state(GameState.GAME_OVER, 
                                                 score=abs(int(self.camera_y)), 
                                                 reason="Victory")
    
    def check_platform_collisions(self):
        """Check for collisions between player and platforms"""
        # Only check if player is moving downward (falling)
        if self.player.vel_y > 0:
            for platform in self.current_map.platforms:
                # Calculate platform's screen position for clarity
                platform_screen_y = platform.y
                
                # Simple AABB collision detection
                if (self.player.y + self.player.radius > platform_screen_y and 
                    self.player.y - self.player.radius < platform_screen_y + platform.height and
                    self.player.x + self.player.radius > platform.x and 
                    self.player.x - self.player.radius < platform.x + platform.width):
                    
                    # Only collide if we're above the platform (to prevent side collisions)
                    if self.player.y < platform_screen_y:
                        # Flash the platform in debug mode to show collision
                        if self.debug_mode:
                            platform.is_colliding = True
                        
                        # Check platform type and respond accordingly
                        if platform.__class__.__name__ == "DangerousPlatform":
                            # Game over on dangerous platform
                            self.state_manager.change_state(GameState.GAME_OVER, 
                                                        score=abs(int(self.camera_y)), 
                                                        reason="Danger")
                            return
                        elif platform.__class__.__name__ == "DisappearingPlatform":
                            # Handle disappearing platform
                            platform.jumps_remaining -= 1
                            if platform.jumps_remaining <= 0:
                                self.current_map.platforms.remove(platform)
                        
                        # Land on platform and bounce
                        if self.player.land(platform_screen_y):
                            self.player.bounce()
                            return  # Only bounce on one platform
    
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
            # Show debug info if enabled
            if self.debug_mode:
                self.current_map.draw_platform_info(self.screen, self.camera_y)
                
                # Draw camera position
                font = pygame.font.SysFont(None, 24)
                text = font.render(f"Camera Y: {self.camera_y:.0f}", True, BLACK)
                self.screen.blit(text, (10, 130))
        
        # Draw player
        if self.player:
            # Draw the player at its screen position (no need to adjust for camera since we move the player)
            self.player.draw(self.screen)
            
            # In debug mode, show player position and velocity
            if self.debug_mode:
                font = pygame.font.SysFont(None, 24)
                text = font.render(f"Player: ({self.player.x:.0f}, {self.player.y:.0f}) Vel: ({self.player.vel_x:.1f}, {self.player.vel_y:.1f})", True, BLACK)
                self.screen.blit(text, (10, 160))
        
        # Draw score
        font = pygame.font.SysFont(None, 36)
        score = self.state_manager.get_state_data("score")
        text = font.render(f"Score: {score}", True, BLACK)
        self.screen.blit(text, (10, 10))
        
        # Show debug mode indicator
        if self.debug_mode:
            font = pygame.font.SysFont(None, 24)
            text = font.render("DEBUG MODE (F1 to toggle)", True, (255, 0, 0))
            self.screen.blit(text, (self.width - text.get_width() - 10, 10))
    
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