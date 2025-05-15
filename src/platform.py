import pygame
from src.constants import GREEN, RED, BLUE, YELLOW

class Platform:
    def __init__(self, x, y, width=100, height=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = GREEN
        
    def update(self):
        # Will be implemented in derived classes
        pass
        
    def draw(self, screen):
        # Draw the platform
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
class MovingPlatform(Platform):
    def __init__(self, x, y, width=100, height=10, move_speed=2, move_range=100):
        super().__init__(x, y, width, height)
        self.color = BLUE
        self.move_speed = move_speed
        self.move_range = move_range
        self.start_x = x
        self.direction = 1  # 1 for right, -1 for left
        
    def update(self):
        # Move the platform back and forth
        pass
        
class DisappearingPlatform(Platform):
    def __init__(self, x, y, width=100, height=10, jump_limit=2):
        super().__init__(x, y, width, height)
        self.color = YELLOW
        self.jumps_remaining = jump_limit
        
    def update(self):
        # Update appearance based on jumps_remaining
        pass
        
    def draw(self, screen):
        # Draw the platform with jump counter
        super().draw(screen)
        # Will add jump counter text later
        
class DangerousPlatform(Platform):
    def __init__(self, x, y, width=100, height=10):
        super().__init__(x, y, width, height)
        self.color = RED 