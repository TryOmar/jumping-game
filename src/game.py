import pygame
import sys
from src.constants import WHITE, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, GREEN, BLUE, YELLOW, RED
from src.game_state import GameState, StateManager
from src.player import Player
from src.map import Map
from src.platform import Platform, MovingPlatform, DisappearingPlatform, DangerousPlatform
from src.renderers.base_renderer import BaseRenderer
from src.event_handler import EventHandler
from src.collision_handler import CollisionHandler
from src.config.settings import get_setting, update_setting

class Game:
    def __init__(self, width=800, height=600, fps=60):
        # Initialize pygame mixer for sound
        pygame.mixer.init()
        
        # Game window settings
        self.width = width
        self.height = height
        self.fps = fps
        
        # Setup game window
        fullscreen = get_setting('WINDOW', 'fullscreen', False)
        flags = pygame.FULLSCREEN if fullscreen else 0
        self.screen = pygame.display.set_mode((self.width, self.height), flags)
        pygame.display.set_caption("Jumping Ball Game")
        self.clock = pygame.time.Clock()
        
        # Initialize state management
        self.state_manager = StateManager()
        
        # Initialize game objects (will be created properly when starting game)
        self.player = None
        self.current_map = None
        self.camera_y = 0
        
        # Audio settings
        self.setup_audio()
        
        # Debug mode
        self.debug_mode = False
        
        # Auto-jump message display
        self.show_auto_jump_message = False
        self.auto_jump_message_time = 0
        self.auto_jump_status = True  # Default is enabled
        
        # Map selection state
        self.map_selection_buttons = {}
        
        # Menu options
        self.menu_options = ["Play", "How to Play", "Settings", "Exit"]
        self.selected_option = 0
        
        # Game over options
        self.game_over_selected_option = 0
        self.game_over_buttons = []
        
        # Game state
        self.running = True
        
        # Initialize handlers
        self.renderer = BaseRenderer(self.screen)
        self.event_handler = EventHandler(self)
        self.collision_handler = CollisionHandler(self)
    
    def setup_audio(self):
        """Setup audio system with current settings"""
        # Get volume settings
        master_volume = get_setting('AUDIO', 'master_volume', 1.0)
        sfx_volume = get_setting('AUDIO', 'sfx_volume', 1.0)
        music_volume = get_setting('AUDIO', 'music_volume', 0.7)
        
        # Set global volumes
        pygame.mixer.music.set_volume(music_volume * master_volume)
        
        # Store sounds dictionary (to be filled when sounds are loaded)
        self.sounds = {}
        
    def handle_events(self):
        """Process all game events using the event handler"""
        self.event_handler.handle_events()
    
    def init_game(self, custom_settings=None):
        """
        Initialize game objects for a new game
        
        Args:
            custom_settings (dict, optional): Custom settings for the game
        """
        # Create player with default or custom settings
        if custom_settings:
            # Apply custom settings to player
            player_speed = custom_settings.get("player_speed", 5)
            jump_strength = custom_settings.get("jump_strength", 10)
            self.player = Player(self.width // 2, self.height - 100, 
                                speed=player_speed, 
                                jump_strength=jump_strength)
            
            # Pass gravity to player
            gravity = custom_settings.get("gravity", 0.5)
            self.player.gravity = gravity
        else:
            # Use default settings
            self.player = Player(self.width // 2, self.height - 100)
        
        # Create map with default or custom settings
        if custom_settings:
            # Create map with custom settings
            platform_density = custom_settings.get("platform_density", 2.0)
            moving_pct = custom_settings.get("moving_platform_pct", 25)
            disappearing_pct = custom_settings.get("disappearing_platform_pct", 15)
            dangerous_pct = custom_settings.get("dangerous_platform_pct", 10)
            
            self.current_map = Map(
                platform_density=platform_density,
                moving_platform_pct=moving_pct,
                disappearing_platform_pct=disappearing_pct,
                dangerous_platform_pct=dangerous_pct
            )
        else:
            self.current_map = Map()
            
        # Generate initial platforms
        self.current_map.generate_map()
        
        # Reset camera position
        self.camera_y = 0
        
        # Initialize score
        self.state_manager.set_state_data("score", 0)
        
        # Store custom settings in state data if provided
        if custom_settings:
            self.state_manager.set_state_data("custom_settings", custom_settings)
    
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
                self.collision_handler.check_platform_collisions() # Use collision handler
                
                if self.camera_y <= self.current_map.target_height:
                    self.state_manager.change_state(GameState.GAME_OVER, 
                                                 score=abs(int(self.camera_y)), 
                                                 reason="Victory")
    
    def toggle_debug(self):
        """Toggle debug visualization"""
        self.debug_mode = not self.debug_mode
        
        # Also pass debug mode to map
        if self.current_map:
            self.current_map.debug_mode = self.debug_mode
    
    def render(self):
        """Draw everything to the screen using the renderer"""
        self.renderer.render(self)
    
    def apply_audio_settings(self):
        """Apply current audio settings"""
        # Get volume settings
        master_volume = get_setting('AUDIO', 'master_volume', 1.0)
        sfx_volume = get_setting('AUDIO', 'sfx_volume', 1.0)
        music_volume = get_setting('AUDIO', 'music_volume', 0.7)
        
        # Apply music volume
        pygame.mixer.music.set_volume(music_volume * master_volume)
        
        # Apply sfx volume to all sounds
        for sound in self.sounds.values():
            sound.set_volume(sfx_volume * master_volume)
    
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