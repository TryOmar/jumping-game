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
        
    def update(self):
        # This will handle player movement and physics
        pass
        
    def jump(self):
        # This will handle jumping
        pass
        
    def shoot(self):
        # This will handle shooting
        pass
        
    def move_left(self):
        # This will handle left movement
        pass
        
    def move_right(self):
        # This will handle right movement
        pass
        
    def draw(self, screen):
        # Draw the player
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius) 