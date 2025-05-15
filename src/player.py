import pygame
from src.constants import BLACK, GRAVITY, JUMP_STRENGTH, MOVE_SPEED

class Player:
    def __init__(self, x, y, radius=15):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = BLACK
        
        # Physics properties
        self.vel_x = 0
        self.vel_y = 0
        self.is_jumping = False
        self.on_ground = False
        self.jump_strength = JUMP_STRENGTH
        self.gravity = GRAVITY
        self.move_speed = MOVE_SPEED
        
        # For automatic jumping
        self.auto_jump_cooldown = 0
        
    def update(self):
        """Update player position and physics"""
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
        
        # Check if we've landed on a platform
        # This will be handled by the collision detection in the game
        
    def jump(self, force=None):
        """Make the player jump"""
        if self.on_ground or force:
            # Apply jump velocity
            if force:
                self.vel_y = force
            else:
                self.vel_y = self.jump_strength
            self.is_jumping = True
            self.on_ground = False
            self.auto_jump_cooldown = 10  # Short cooldown to prevent double jumps
            return True
        return False
        
    def bounce(self, strength=None):
        """Bounce the player (automatic jump when hitting platforms)"""
        # Only allow bounce if cooldown is not active
        if self.auto_jump_cooldown <= 0:
            # Increased bounce height significantly
            bounce_strength = strength if strength is not None else self.jump_strength * 1.2
            self.vel_y = bounce_strength
            self.is_jumping = True
            self.on_ground = False
            return True
        return False
        
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
        
    def land(self, platform_y):
        """Called when player lands on a platform"""
        # Prevent player from going through the platform
        self.y = platform_y - self.radius
        self.vel_y = 0
        self.is_jumping = False
        self.on_ground = True
        
        # Return True if we need to trigger automatic bounce
        return True
                
    def draw(self, screen):
        """Draw the player"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius) 