import pygame
import random
from src.platform import Platform, MovingPlatform, DisappearingPlatform, DangerousPlatform
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLATFORM_COUNT

class Map:
    def __init__(self, theme_color=(0, 150, 0), gravity=0.5, platform_speed=2):
        self.platforms = []
        self.theme_color = theme_color
        self.gravity = gravity
        self.platform_speed = platform_speed
        self.target_height = -5000  # Negative because we'll be going up
        
    def generate_map(self):
        """Generate the initial platforms for the map"""
        # Clear any existing platforms
        self.platforms = []
        
        # Create a starter platform at the bottom
        start_platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, width=100)
        self.platforms.append(start_platform)
        
        # Generate random platforms going upward
        for i in range(PLATFORM_COUNT):
            # Random placement - ensure some vertical spacing
            x = random.randint(10, SCREEN_WIDTH - 110)
            y = SCREEN_HEIGHT - 100 - i * (SCREEN_HEIGHT / PLATFORM_COUNT)
            
            # Randomize platform type with weights
            platform_type = random.choices(
                ["regular", "moving", "disappearing", "dangerous"],
                weights=[0.6, 0.2, 0.15, 0.05],
                k=1
            )[0]
            
            # Create the appropriate platform type
            if platform_type == "regular":
                platform = Platform(x, y)
            elif platform_type == "moving":
                platform = MovingPlatform(x, y, move_speed=self.platform_speed)
            elif platform_type == "disappearing":
                platform = DisappearingPlatform(x, y)
            elif platform_type == "dangerous":
                platform = DangerousPlatform(x, y)
            
            self.platforms.append(platform)
        
    def update(self, camera_y):
        """Update all platforms, remove off-screen ones, generate new ones"""
        # Update platforms based on type
        for platform in self.platforms:
            platform.update()
            
        # Remove platforms that are below the bottom of the screen
        self.platforms = [p for p in self.platforms if p.y < SCREEN_HEIGHT - camera_y + 50]
        
        # If we're running low on platforms, generate more above
        if len(self.platforms) < PLATFORM_COUNT / 2:
            self.generate_more_platforms(camera_y)
    
    def generate_more_platforms(self, camera_y):
        """Generate additional platforms as the player moves up"""
        # Find the highest platform
        highest_y = min([p.y for p in self.platforms]) if self.platforms else SCREEN_HEIGHT
        
        # Generate new platforms above the highest one
        for i in range(5):  # Add 5 new platforms
            # Random placement with spacing
            x = random.randint(10, SCREEN_WIDTH - 110)
            y = highest_y - 100 - i * 100
            
            # Randomize platform type with weights
            platform_type = random.choices(
                ["regular", "moving", "disappearing", "dangerous"],
                weights=[0.6, 0.2, 0.15, 0.05],
                k=1
            )[0]
            
            # Create the appropriate platform type
            if platform_type == "regular":
                platform = Platform(x, y)
            elif platform_type == "moving":
                platform = MovingPlatform(x, y, move_speed=self.platform_speed)
            elif platform_type == "disappearing":
                platform = DisappearingPlatform(x, y)
            elif platform_type == "dangerous":
                platform = DangerousPlatform(x, y)
            
            self.platforms.append(platform)
            
    def draw(self, screen, camera_y):
        """Draw all platforms with camera offset"""
        for platform in self.platforms:
            # Adjust platform position based on camera
            rect = pygame.Rect(platform.x, platform.y - camera_y, platform.width, platform.height)
            
            # Only draw if on screen
            if rect.bottom >= 0 and rect.top <= SCREEN_HEIGHT:
                pygame.draw.rect(screen, platform.color, rect)
                
                # Draw counter for disappearing platforms
                if isinstance(platform, DisappearingPlatform) and platform.jumps_remaining > 0:
                    font = pygame.font.SysFont(None, 20)
                    text = font.render(str(platform.jumps_remaining), True, (0, 0, 0))
                    screen.blit(text, (rect.centerx - text.get_width()//2, 
                                     rect.centery - text.get_height()//2))
            
    def check_collision(self, player):
        # Check if player collides with any platform
        pass 