import pygame
import random
from src.constants import WHITE, BLACK, RED, GREEN, BLUE, YELLOW, SCREEN_WIDTH, PLATFORM_WIDTH, PLATFORM_HEIGHT

class Platform:
    """Base platform class"""
    id_counter = 0
    
    def __init__(self, x, y, width, height, color=None):
        """Initialize platform"""
        Platform.id_counter += 1
        self.id = Platform.id_counter
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color or GREEN
        self.colliding = False  # Flag for collision detection visualization
        self.collision_timer = 0
        
    def update(self, camera_y):
        """Update platform"""
        # Reset collision visualization after a few frames
        if self.colliding:
            self.collision_timer += 1
            if self.collision_timer > 5:  # Reset after 5 frames
                self.colliding = False
                self.collision_timer = 0
        
    def on_collision(self, player):
        """Handle collision with player"""
        # Base platform just stops the player
        # Set the collision flag for visualization
        self.colliding = True
        self.collision_timer = 0
        pass

    def draw(self, screen):
        # This is handled by the Map class now
        pass
        
class MovingPlatform(Platform):
    """Platform that moves horizontally"""
    
    def __init__(self, x, y, width, height, color=None, speed=None):
        """Initialize moving platform"""
        super().__init__(x, y, width, height, color or BLUE)
        self.speed = speed or random.uniform(1, 3)
        self.direction = random.choice([-1, 1])
        self.start_x = x
        
    def update(self, camera_y):
        """Update platform position"""
        # Move horizontally
        self.x += self.speed * self.direction
        
        # Bounce off edges (assume screen width from constants)
        screen_width = 800  # Default value
        if 'SCREEN_WIDTH' in globals():
            screen_width = SCREEN_WIDTH
            
        if self.x <= 0:
            self.x = 0
            self.direction = 1
        elif self.x + self.width >= screen_width:
            self.x = screen_width - self.width
            self.direction = -1
            
        # Reset collision visualization
        super().update(camera_y)
        
    def draw(self, screen):
        # Draw the platform
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
class DisappearingPlatform(Platform):
    """Platform that disappears after player jumps from it"""
    
    def __init__(self, x, y, width, height, color=None, jumps=None):
        """Initialize disappearing platform"""
        super().__init__(x, y, width, height, color or (255, 200, 0))  # Orange
        self.jumps_remaining = jumps or 1  # How many jumps before it disappears
        self.original_color = color or (255, 200, 0)
        
    def on_collision(self, player):
        """Handle collision with player"""
        # Reduce number of jumps remaining
        self.jumps_remaining -= 1
        # Set the collision flag
        self.colliding = True
        self.collision_timer = 0
        
    def should_remove(self):
        """Check if platform should be removed"""
        return self.jumps_remaining <= 0

    def update(self, camera_y):
        # No movement, but update the color based on remaining jumps
        if self.jumps_remaining == 2:
            self.color = self.original_color
        elif self.jumps_remaining == 1:
            self.color = (255, 200, 0)  # Darker yellow
        
        # Reset collision visualization
        super().update(camera_y)
        
    def draw(self, screen):
        # This is now handled by the Map class
        pass
        
class DangerousPlatform(Platform):
    """Platform that causes player to die"""
    
    def __init__(self, x, y, width, height, color=None):
        """Initialize dangerous platform"""
        super().__init__(x, y, width, height, color or RED)
    
    def on_collision(self, player):
        """Handle collision with player"""
        # In game.py, we'll trigger game over state
        self.colliding = True
        self.collision_timer = 0
        pass

    def update(self, camera_y):
        # Reset collision visualization
        super().update(camera_y) 