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
        self.y = y # World Y coordinate
        self.width = width
        self.height = height
        self.color = color or GREEN
        self.colliding = False
        self.collision_timer = 0
        self.bounce_ready = True
        self.last_collision_time = 0  # Track when last collision occurred
        
    def update(self, camera_y):
        """Update platform"""
        if self.colliding:
            self.collision_timer += 1
            if self.collision_timer > 5:
                self.colliding = False
                self.collision_timer = 0
        
        # Reset bounce_ready flag after a short cooldown, even if player is still on platform
        # This allows bouncing on the same platform multiple times
        if not self.bounce_ready and pygame.time.get_ticks() - self.last_collision_time > 300:  # 300ms cooldown
            self.bounce_ready = True
        
    def on_collision(self, player):
        """Handle collision with player"""
        self.colliding = True
        self.collision_timer = 0
        self.bounce_ready = False  # Mark as not ready for bounce until reset
        self.last_collision_time = pygame.time.get_ticks()
        pass

    # draw() method removed as Map.draw handles platform drawing
        
class MovingPlatform(Platform):
    """Platform that moves horizontally"""
    
    def __init__(self, x, y, width, height, color=None, speed=None):
        """Initialize moving platform"""
        super().__init__(x, y, width, height, color or BLUE)
        self.speed = speed or random.uniform(1, 3)
        self.direction = random.choice([-1, 1])
        self.start_x = x # Not currently used, but might be useful for defined paths
        
    def update(self, camera_y):
        """Update platform position"""
        self.x += self.speed * self.direction
        
        # Using SCREEN_WIDTH directly from constants for boundary check
        if self.x <= 0:
            self.x = 0
            self.direction = 1
        elif self.x + self.width >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
            self.direction = -1
            
        super().update(camera_y)
        
    # draw() method removed
        
class DisappearingPlatform(Platform):
    """Platform that disappears after player jumps from it"""
    
    def __init__(self, x, y, width, height, color=None, jumps=None):
        """Initialize disappearing platform"""
        super().__init__(x, y, width, height, color or (255, 200, 0)) # Orange
        self.jumps_remaining = jumps or 1
        self.original_color = self.color # Store the initial color for multi-jump platforms
    
    def on_collision(self, player):
        """Handle collision with player"""
        self.jumps_remaining -= 1
        self.colliding = True
        self.collision_timer = 0
        
    def should_remove(self):
        """Check if platform should be removed"""
        return self.jumps_remaining <= 0

    def update(self, camera_y):
        # Update color based on remaining jumps (example for 2 jumps)
        if self.jumps_remaining == 2:
             self.color = self.original_color # Or a specific color for 2 jumps left
        elif self.jumps_remaining == 1:
            # Change color to indicate one jump left, if not already the final color
            if self.original_color != (200, 150, 0): # Avoid re-coloring if it started dark
                 self.color = (200, 150, 0) # Darker orange/yellow
        elif self.jumps_remaining <= 0:
            # Could make it more transparent or a different color before removal
            pass # Removal is handled by Map class based on should_remove()
        
        super().update(camera_y)
        
    # draw() method removed
        
class DangerousPlatform(Platform):
    """Platform that causes player to die"""
    
    def __init__(self, x, y, width, height, color=None):
        """Initialize dangerous platform"""
        super().__init__(x, y, width, height, color or RED)
    
    # on_collision and update are inherited or simple pass-through
    # draw() method removed 