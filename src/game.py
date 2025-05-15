import pygame
import sys
from src.constants import WHITE, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT
from src.game_state import GameState, StateManager
from src.player import Player
from src.map import Map
from src.platform import Platform, MovingPlatform, DisappearingPlatform, DangerousPlatform

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
        
        # Auto-jump message display
        self.show_auto_jump_message = False
        self.auto_jump_message_time = 0
        self.auto_jump_status = True  # Default is enabled
        
        # Menu options
        self.menu_options = ["Play", "How to Play", "Settings", "Exit"]
        self.selected_option = 0
        
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
                    self.toggle_debug()
                
                # Toggle auto-jump with J key
                if event.key == pygame.K_j and self.player:
                    enabled = self.player.toggle_auto_jump()
                    status = "enabled" if enabled else "disabled"
                    print(f"Auto-jump {status}")
                    
                    # Add visual feedback when auto-jump is toggled
                    self.show_auto_jump_message = True
                    self.auto_jump_message_time = pygame.time.get_ticks()
                    self.auto_jump_status = enabled
                
                # Main menu controls
                if self.state_manager.is_state(GameState.MAIN_MENU):
                    if event.key == pygame.K_UP:
                        self.selected_option = max(0, self.selected_option - 1)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = min(len(self.menu_options) - 1, self.selected_option + 1)
                    elif event.key == pygame.K_RETURN:
                        self._handle_menu_selection()
                
                # Temporary state change keys for testing
                if event.key == pygame.K_1:
                    self.state_manager.change_state(GameState.MAIN_MENU)
                elif event.key == pygame.K_2:
                    # Always reinitialize the game when starting a new game
                    self.state_manager.change_state(GameState.PLAYING)
                    self.init_game()
                elif event.key == pygame.K_3:
                    self.state_manager.change_state(GameState.GAME_OVER, score=100)
            
            # Handle mouse events for menu
            if self.state_manager.is_state(GameState.MAIN_MENU):
                if event.type == pygame.MOUSEMOTION:
                    # Check if mouse is over any menu option
                    mouse_pos = pygame.mouse.get_pos()
                    for i, option in enumerate(self.menu_options):
                        option_rect = self._get_menu_option_rect(i)
                        if option_rect.collidepoint(mouse_pos):
                            self.selected_option = i
                            break
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    # Check if clicking on a menu option
                    mouse_pos = pygame.mouse.get_pos()
                    for i, option in enumerate(self.menu_options):
                        option_rect = self._get_menu_option_rect(i)
                        if option_rect.collidepoint(mouse_pos):
                            self.selected_option = i
                            self._handle_menu_selection()
                            break
    
    def _handle_menu_selection(self):
        """Handle menu option selection"""
        if self.selected_option == 0:  # Play
            self.state_manager.change_state(GameState.PLAYING)
            self.init_game()
        elif self.selected_option == 1:  # How to Play
            self.state_manager.change_state(GameState.HOW_TO_PLAY)
        elif self.selected_option == 2:  # Settings
            self.state_manager.change_state(GameState.SETTINGS)
        elif self.selected_option == 3:  # Exit
            self.running = False
    
    def _get_menu_option_rect(self, index):
        """Get the rectangle for a menu option for collision detection"""
        option_height = 40
        start_y = self.height // 2
        option_y = start_y + index * option_height
        
        # Approximate width based on text length
        option_width = len(self.menu_options[index]) * 20
        option_x = self.width // 2 - option_width // 2
        
        return pygame.Rect(option_x, option_y, option_width, option_height)
    
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
            if self.player and self.current_map:
                keys = pygame.key.get_pressed()
                self.player.handle_input(keys)
                self.player.update() # Player position (world) updated by physics

                if self.player.x < 0:
                    self.player.x = self.width
                elif self.player.x > self.width:
                    self.player.x = 0
                
                # Camera scrolling logic based on player's screen position
                player_screen_y = self.player.y - self.camera_y
                scroll_threshold_screen = self.height // 3

                if player_screen_y < scroll_threshold_screen:
                    # Calculate how much the camera needs to move up to keep the player at the threshold
                    camera_scroll_amount = scroll_threshold_screen - player_screen_y
                    self.camera_y -= camera_scroll_amount # Camera moves up (camera_y becomes more negative)
                    # Player's world_y is NOT changed by camera scroll; physics handles player world movement.
                    # The previous self.player.y += camera_shift was an attempt to keep player screen-relative,
                    # but it's better if player.y is pure world and camera adjusts around it.

                    self.state_manager.set_state_data("score", abs(int(self.camera_y)))
                
                # Check if player has fallen off the bottom of the screen
                player_screen_y_for_fall_check = self.player.y - self.camera_y
                if player_screen_y_for_fall_check > self.height + self.player.radius: # Added radius for buffer
                    self.state_manager.change_state(GameState.GAME_OVER, 
                                                 score=abs(int(self.camera_y)), 
                                                 reason="Fall")
                
                self.current_map.update(self.camera_y)
                self.check_platform_collisions() # Uses world coordinates
                
                if self.camera_y <= self.current_map.target_height:
                    self.state_manager.change_state(GameState.GAME_OVER, 
                                                 score=abs(int(self.camera_y)), 
                                                 reason="Victory")
    
    def check_platform_collisions(self):
        """Check for collisions between player and platforms"""
        if not self.player or not self.current_map:
            return

        # Reset all platform collision flags
        for platform in self.current_map.platforms:
            # Don't reset platform.colliding here, let platforms manage their own state
            pass

        # Get platforms the player might be colliding with
        colliding_platforms = []
        for platform in self.current_map.platforms:
            # Only check for collision if we're falling onto a platform
            # Small modification: allow collision if player is at peak of jump (vel_y near zero)
            # or falling (vel_y positive), but not when rising quickly
            if self.player.vel_y < -2:  # Only avoid collision when player is rising quickly
                continue
                
            # Ensure the player's feet are at or below the top of the platform
            # This makes the collision detection more forgiving
            foot_y = self.player.y + self.player.radius
            if foot_y < platform.y - 2:  # Small tolerance
                continue
            
            # Complete collision check - AABB with circle
            if (self.player.y + self.player.radius > platform.y and 
                self.player.y - self.player.radius < platform.y + platform.height and
                self.player.x + self.player.radius > platform.x and 
                self.player.x - self.player.radius < platform.x + platform.width):
                
                # Check if the player is falling onto the platform (not rising through it)
                # Increased tolerance for better bouncing
                if foot_y >= platform.y and foot_y <= platform.y + 15:  # 15 pixels of tolerance
                    colliding_platforms.append(platform)
                    platform.colliding = True  # Set collision flag for visualization
        
        # Handle collision with the highest platform if there are multiple
        if colliding_platforms:
            # Find the highest platform (lowest y value)
            highest_platform = min(colliding_platforms, key=lambda p: p.y)
            
            # Debug info
            if self.debug_mode:
                print(f"Collision with platform {highest_platform.id} at world Y: {highest_platform.y}")
            
            # Place player on top of platform and set on_ground
            self.player.land(highest_platform.y)
            
            # Handle platform special effects
            self.handle_platform_effect(highest_platform)
    
    def toggle_debug(self):
        """Toggle debug visualization"""
        self.debug_mode = not self.debug_mode
        
        # Also pass debug mode to map
        if self.current_map:
            self.current_map.debug_mode = self.debug_mode
    
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
        # Draw background
        background_color = (50, 100, 150)  # Nice blue background
        self.screen.fill(background_color)
        
        # Draw game title
        title_font = pygame.font.SysFont(None, 72)
        title_text = title_font.render("JUMPING BALL", True, WHITE)
        self.screen.blit(title_text, (self.width//2 - title_text.get_width()//2, 100))
        
        # Draw decorative circles
        pygame.draw.circle(self.screen, BLACK, (self.width//2, 200), 30)
        pygame.draw.circle(self.screen, (200, 200, 0), (self.width//2 - 80, 220), 15)
        pygame.draw.circle(self.screen, (0, 200, 200), (self.width//2 + 80, 220), 15)
        
        # Draw menu options
        option_height = 40
        start_y = self.height // 2
        
        for i, option in enumerate(self.menu_options):
            # Determine if this option is selected
            is_selected = (i == self.selected_option)
            
            # Choose font color based on selection
            color = BLACK if not is_selected else (255, 0, 0)
            
            # Create option text
            option_font = pygame.font.SysFont(None, 36)
            option_text = option_font.render(option, True, color)
            
            # Draw option text
            option_y = start_y + i * option_height
            option_x = self.width//2 - option_text.get_width()//2
            self.screen.blit(option_text, (option_x, option_y))
            
            # Draw indicator if selected
            if is_selected:
                # Draw arrow or highlight
                pygame.draw.polygon(self.screen, (255, 0, 0), [
                    (option_x - 20, option_y + option_text.get_height()//2),
                    (option_x - 10, option_y + option_text.get_height()//2 - 5),
                    (option_x - 10, option_y + option_text.get_height()//2 + 5),
                ])
        
        # Draw footer text
        footer_font = pygame.font.SysFont(None, 20)
        footer_text = footer_font.render("Use arrow keys to select, Enter to confirm", True, WHITE)
        self.screen.blit(footer_text, (self.width//2 - footer_text.get_width()//2, self.height - 50))
    
    def _render_map_select(self):
        """Render the map selection screen"""
        # Will be implemented later
        pass
    
    def _render_game(self):
        """Render the actual gameplay"""
        if self.current_map:
            self.current_map.draw(self.screen, self.camera_y)
            if self.debug_mode:
                self.current_map.draw_platform_info(self.screen, self.camera_y)
                font = pygame.font.SysFont(None, 24)
                text = font.render(f"Camera Y (World): {self.camera_y:.0f}", True, BLACK)
                self.screen.blit(text, (10, 130))
                coord_text = font.render("World Y → Screen Y (World Y - Camera Y)", True, BLACK)
                self.screen.blit(coord_text, (10, 190))
        
        if self.player:
            self.player.draw(self.screen, self.camera_y) # Pass camera_y
            
            if self.debug_mode:
                font = pygame.font.SysFont(None, 24)
                player_screen_y_debug = self.player.y - self.camera_y
                text = font.render(f"Player (World Y): {self.player.y:.0f} (Screen Y): {player_screen_y_debug:.0f}", True, BLACK)
                self.screen.blit(text, (10, 160))
                vel_text = font.render(f"Vel: ({self.player.vel_x:.1f}, {self.player.vel_y:.1f})", True, BLACK)
                self.screen.blit(vel_text, (10, 175)) # Adjusted y for new line
                jump_text = font.render(f"On Ground: {self.player.on_ground} | Jumping: {self.player.is_jumping} | Cool: {self.player.auto_jump_cooldown}", True, BLACK)
                self.screen.blit(jump_text, (10, 220))
                auto_jump_text = font.render(f"Auto-Jump: {'ON' if self.player.auto_jump_enabled else 'OFF'}", True, (0, 128, 0) if self.player.auto_jump_enabled else (200, 0, 0))
                self.screen.blit(auto_jump_text, (10, 240))
        
        font = pygame.font.SysFont(None, 36)
        score = self.state_manager.get_state_data("score")
        text = font.render(f"Score: {score}", True, BLACK)
        self.screen.blit(text, (10, 10))
        
        # Show auto-jump toggle instructions and status
        font_small = pygame.font.SysFont(None, 24)
        auto_status = "ON" if self.player and self.player.auto_jump_enabled else "OFF"
        status_color = (0, 128, 0) if self.player and self.player.auto_jump_enabled else (200, 0, 0)
        text = font_small.render(f"Auto-Jump: {auto_status} (Press J to toggle)", True, status_color)
        self.screen.blit(text, (10, 45))
        
        # Display auto-jump toggle message if active
        if self.show_auto_jump_message:
            # Check if message should still be displayed (show for 2 seconds)
            current_time = pygame.time.get_ticks()
            if current_time - self.auto_jump_message_time < 2000:  # 2000ms = 2s
                # Create a semi-transparent background for the message
                msg_surface = pygame.Surface((400, 80), pygame.SRCALPHA)
                msg_surface.fill((0, 0, 0, 128))  # Black with 50% transparency
                
                # Add message text
                msg_font = pygame.font.SysFont(None, 36)
                msg_status = "ENABLED" if self.auto_jump_status else "DISABLED"
                msg_color = (0, 255, 0) if self.auto_jump_status else (255, 0, 0)
                msg_text = msg_font.render(f"Auto-Jump {msg_status}", True, msg_color)
                
                # Center the message on the screen
                msg_x = self.width // 2 - msg_surface.get_width() // 2
                msg_y = self.height // 2 - msg_surface.get_height() // 2
                
                # Draw message background and text
                self.screen.blit(msg_surface, (msg_x, msg_y))
                self.screen.blit(msg_text, (msg_x + 200 - msg_text.get_width() // 2, 
                                          msg_y + 40 - msg_text.get_height() // 2))
            else:
                # Time expired, hide message
                self.show_auto_jump_message = False
        
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
        text1 = font_small.render("Press 1 to return to main menu", True, BLACK)
        text2 = font_small.render("Press 2 to play again", True, BLACK)
        self.screen.blit(text1, (self.width//2 - text1.get_width()//2, self.height//2 + 80))
        self.screen.blit(text2, (self.width//2 - text2.get_width()//2, self.height//2 + 110))
    
    def _render_settings(self):
        """Render settings screen"""
        # Will be implemented later
        pass
    
    def _render_how_to_play(self):
        """Render instructions screen"""
        # Fill background
        self.screen.fill((230, 230, 250))  # Light blue/purple background
        
        # Title
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("How to Play", True, BLACK)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))
        
        # Instructions
        instructions = [
            "Move LEFT and RIGHT with arrow keys",
            "Press UP to jump manually (when auto-jump is off)",
            "Press J to toggle auto-jump mode ON/OFF",
            "Auto-jump: Player jumps automatically when landing on platforms",
            "Bounce on platforms to climb higher and score points",
            "Watch out for red dangerous platforms!",
            "Yellow platforms will disappear after you bounce on them",
            "Blue platforms move horizontally",
            "Don't fall off the bottom of the screen!"
        ]
        
        y_pos = 120
        line_height = 30
        instruction_font = pygame.font.SysFont(None, 28)
        
        for line in instructions:
            text = instruction_font.render(line, True, BLACK)
            self.screen.blit(text, (self.width // 2 - text.get_width() // 2, y_pos))
            y_pos += line_height
        
        # Return to main menu
        back_text = instruction_font.render("Press ESC to return to main menu", True, BLACK)
        self.screen.blit(back_text, (self.width // 2 - back_text.get_width() // 2, self.height - 50))
    
    def handle_platform_effect(self, platform):
        """Handle special effects for different platform types"""
        # Call the platform's collision handler
        platform.on_collision(self.player)
        
        # Make the player bounce
        # Always bounce if platform is bounce_ready or if player is falling
        # onto a platform (vel_y > 0)
        # This ensures consistent bouncing regardless of auto-jump settings
        if self.player.vel_y > 0 or platform.bounce_ready:
            self.player.bounce()
        
        # Handle platform type specific effects
        if isinstance(platform, DangerousPlatform):
            # Game over on dangerous platform
            self.state_manager.change_state(GameState.GAME_OVER, 
                                         score=abs(int(self.camera_y)), 
                                         reason="Danger")
        elif isinstance(platform, DisappearingPlatform):
            # Check if platform should be removed
            if platform.should_remove():
                self.current_map.platforms.remove(platform) 