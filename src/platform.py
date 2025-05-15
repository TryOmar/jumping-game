import pygame
from src.constants import GREEN, RED, BLUE, YELLOW, SCREEN_WIDTH

class Platform:
    def __init__(self, x, y, width=100, height=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = GREEN
        
    def update(self):
        # Base platforms don't move
        pass
        
    def draw(self, screen):
        # This is handled by the Map class now
        pass
        
class MovingPlatform(Platform):
    def __init__(self, x, y, width=100, height=10, move_speed=2, move_range=100):
        super().__init__(x, y, width, height)
        self.color = BLUE
        self.move_speed = move_speed
        self.move_range = move_range
        self.start_x = x
        self.direction = 1  # 1 for right, -1 for left
        
    def update(self):
        # Move the platform back and forth horizontally
        self.x += self.move_speed * self.direction
        
        # Change direction if we've moved too far
        if self.x > self.start_x + self.move_range:
            self.direction = -1
        elif self.x < self.start_x - self.move_range:
            self.direction = 1
            
        # Handle edge cases (screen boundaries)
        if self.x < 0:
            self.x = 0
            self.direction = 1
        elif self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
            self.direction = -1
        
    def draw(self, screen):
        # Draw the platform
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
class DisappearingPlatform(Platform):
    def __init__(self, x, y, width=100, height=10, jump_limit=2):
        super().__init__(x, y, width, height)
        self.color = YELLOW
        self.jumps_remaining = jump_limit
        
    def update(self):
        # No movement, but will be removed after jumps_remaining reaches 0
        # This is handled in the Game's collision detection
        pass
        
    def draw(self, screen):
        # This is now handled by the Map class
        pass
        
class DangerousPlatform(Platform):
    def __init__(self, x, y, width=100, height=10):
        super().__init__(x, y, width, height)
        self.color = RED 