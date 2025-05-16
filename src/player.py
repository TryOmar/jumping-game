import pygame
from src.constants import BLACK, GRAVITY, JUMP_STRENGTH, MOVE_SPEED

class Player:
    def __init__(self, x, y, radius=15, speed=None, jump_strength=None):
        self.x = x
        self.y = y  # World Y coordinate
        self.radius = radius
        self.color = BLACK
        
        # Physics properties
        self.vel_x = 0
        self.vel_y = 0
        self.is_jumping = False
        self.on_ground = False
        self.jump_strength = jump_strength if jump_strength is not None else JUMP_STRENGTH
        self.gravity = GRAVITY
        self.move_speed = speed if speed is not None else MOVE_SPEED
        
        # For automatic jumping
        self.auto_jump_cooldown = 0
        self.auto_jump_enabled = True  # Flag to enable/disable auto-jumping
        
        # Game reference (set after creation)
        self.game = None
        
        # Landing sound flag
        self.landing_sound_played = False
        
    def set_game(self, game):
        """Set a reference to the game instance for sounds and other interactions"""
        self.game = game
        
    def update(self):
        """Update player position and physics (all in world coordinates)"""
        # Apply gravity
        self.vel_y += self.gravity
        
        # Update position based on velocity
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Apply friction
        self.vel_x *= 0.9
        
        # Reset auto jump cooldown if it's active
        if self.auto_jump_cooldown > 0:
            self.auto_jump_cooldown -= 1
            
        # Auto-jump when on ground and cooldown is over
        if self.auto_jump_enabled and self.on_ground and self.auto_jump_cooldown <= 0:
            self.jump(auto=True)  # Pass auto=True to indicate this is from auto-jump
        
        # Reset landing sound flag if not on ground
        if not self.on_ground:
            self.landing_sound_played = False
        
        # Check if we've landed on a platform
        # This will be handled by the collision detection in the game
        
    def jump(self, force=None, auto=False):
        """Make the player jump"""
        # Allow jump in these cases:
        # 1. If on ground and auto-jump is disabled (manual jump)
        # 2. If auto=True parameter is passed (from auto-jump feature)
        # 3. If force parameter is passed (for special jumps)
        if (self.on_ground and (not self.auto_jump_enabled or auto or force)) or force:
            # Apply jump velocity
            if force:
                self.vel_y = force
            else:
                self.vel_y = -self.jump_strength  # Negative because up is negative in pygame
            self.is_jumping = True
            self.on_ground = False
            self.auto_jump_cooldown = 10  # Short cooldown to prevent double jumps
            
            # Play jump sound if game reference exists
            if self.game and hasattr(self.game, 'sound_manager'):
                self.game.sound_manager.play_game_sound("jump")
                
            return True
        return False
        
    def bounce(self, strength=None):
        """Bounce the player (automatic jump when hitting platforms)"""
        # Always allow bounce from platforms (platform bounce_ready property will control this)
        # Bounce should work regardless of auto-jump settings
        bounce_strength = strength if strength is not None else -self.jump_strength * 1.5
        
        # Directly set velocity without going through jump logic
        # This ensures bouncing always works regardless of auto-jump setting
        self.vel_y = bounce_strength
        self.is_jumping = True
        self.on_ground = False
        
        # Reduced auto_jump_cooldown to allow faster consecutive bounces
        # This way if player falls back onto same platform, they can bounce again immediately
        self.auto_jump_cooldown = 2
        return True
        
    def shoot(self):
        """Shoot a projectile"""
        # Will be implemented later
        pass
        
    def move_left(self):
        """Move player left"""
        self.vel_x = -self.move_speed
        
    def move_right(self):
        """Move player right"""
        self.vel_x = self.move_speed
        
    def handle_input(self, keys):
        """Handle keyboard input for player movement"""
        if keys[pygame.K_LEFT]:
            self.move_left()
        if keys[pygame.K_RIGHT]:
            self.move_right()
        if keys[pygame.K_UP]:
            self.jump()
        
    def reset_landing_sound(self):
        """Reset the landing sound flag"""
        self.landing_sound_played = False
        
    def land(self, platform_world_y):
        """Called when player lands on a platform. platform_world_y is the top of the platform in world coordinates."""
        # Prevent player from going through the platform
        self.y = platform_world_y - self.radius
        self.vel_y = 0
        self.is_jumping = False
        self.on_ground = True
        
        # Reset landing sound flag when landing on a new platform
        self.landing_sound_played = False
        
        # Return True if we need to trigger automatic bounce
        return True
                
    def draw(self, screen, camera_y):
        """Draw the player, converting world coordinates to screen coordinates"""
        player_screen_y = self.y - camera_y
        pygame.draw.circle(screen, self.color, (int(self.x), int(player_screen_y)), self.radius)
        
    def toggle_auto_jump(self):
        """Toggle auto-jump on/off"""
        self.auto_jump_enabled = not self.auto_jump_enabled
        return self.auto_jump_enabled 

    def die(self, reason="Fall"):
        """Handle player death with visual or sound effects"""
        # Play death sound if game reference exists
        if self.game and hasattr(self.game, 'sound_manager'):
            self.game.sound_manager.play_game_sound("die")
            
        # Any additional death effects can be added here
        # Change color, play animation, etc.
        self.color = (255, 0, 0)  # Change to red when dead 

    def reset(self, x=None, y=None):
        """
        Reset the player's state to initial conditions
        
        Args:
            x (float, optional): New x position. If None, keeps current x.
            y (float, optional): New y position. If None, keeps current y.
        """
        # Reset position if new coordinates are provided
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        
        # Reset physics properties
        self.vel_x = 0
        self.vel_y = 0
        self.is_jumping = False
        self.on_ground = False
        
        # Reset sound and jump flags
        self.landing_sound_played = False
        self.auto_jump_cooldown = 0
        
        # Ensure auto-jump is reset to default
        self.auto_jump_enabled = True 