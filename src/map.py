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
        
        # Generate initial platforms going upward with smaller, more consistent gaps
        vertical_gap = 70  # Fixed vertical gap between platforms
        for i in range(PLATFORM_COUNT):
            # Calculate y position with fixed spacing
            y = SCREEN_HEIGHT - 100 - i * vertical_gap
            
            # Ensure good horizontal distribution
            # Divide screen into sections for better distribution
            section_width = SCREEN_WIDTH // 3
            section = i % 3  # 0, 1, or 2
            
            # Random x within the section to ensure platforms across the screen
            min_x = section * section_width + 20
            max_x = (section + 1) * section_width - 120
            x = random.randint(min_x, max_x)
            
            # Randomize platform type with weights
            platform_type = random.choices(
                ["regular", "moving", "disappearing", "dangerous"],
                weights=[0.65, 0.2, 0.1, 0.05],
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
            
        # Remove platforms that are below the bottom of the screen with a margin
        # Only remove platforms that are definitely off-screen
        self.platforms = [p for p in self.platforms if p.y < SCREEN_HEIGHT - camera_y + 200]
        
        # Find the highest platform
        if self.platforms:
            highest_y = min([p.y for p in self.platforms])
            # Always maintain platforms within the visible range and above
            # Ensure there are platforms being generated before they're needed
            screen_top = camera_y
            if highest_y > screen_top - SCREEN_HEIGHT:
                self.generate_more_platforms(camera_y)
    
    def generate_more_platforms(self, camera_y):
        """Generate additional platforms as the player moves up"""
        # Find the highest platform
        highest_y = min([p.y for p in self.platforms]) if self.platforms else SCREEN_HEIGHT
        
        # Generate more platforms with fixed spacing
        vertical_gap = 70  # Same as in generate_map
        platform_count = 8  # Generate more platforms at once for better coverage
        
        for i in range(platform_count):
            # Position each new platform above the highest one with fixed gap
            y = highest_y - (i + 1) * vertical_gap
            
            # Ensure good horizontal distribution
            section_width = SCREEN_WIDTH // 3
            section = i % 3  # 0, 1, or 2
            
            min_x = section * section_width + 20
            max_x = (section + 1) * section_width - 120
            x = random.randint(min_x, max_x)
            
            # Slightly different weights - more stable platforms higher up
            platform_type = random.choices(
                ["regular", "moving", "disappearing", "dangerous"],
                weights=[0.65, 0.2, 0.1, 0.05],
                k=1
            )[0]
            
            # Create platform with consistent width
            platform_width = random.randint(80, 120)  # Vary width slightly
            
            # Create the appropriate platform type
            if platform_type == "regular":
                platform = Platform(x, y, width=platform_width)
            elif platform_type == "moving":
                platform = MovingPlatform(x, y, width=platform_width, move_speed=self.platform_speed)
            elif platform_type == "disappearing":
                platform = DisappearingPlatform(x, y, width=platform_width)
            elif platform_type == "dangerous":
                platform = DangerousPlatform(x, y, width=platform_width)
            
            self.platforms.append(platform)
            
    def draw(self, screen, camera_y):
        """Draw all platforms with camera offset"""
        for platform in self.platforms:
            # Calculate screen position
            screen_y = platform.y - camera_y
            
            # Create rectangle for drawing
            rect = pygame.Rect(platform.x, screen_y, platform.width, platform.height)
            
            # Draw with more generous margin to ensure visibility
            if rect.bottom >= -100 and rect.top <= SCREEN_HEIGHT + 100:
                # Determine platform color (flash if colliding in debug mode)
                color = platform.color
                border_color = (0, 0, 0)  # Default black border
                
                # If platform is colliding, highlight it
                if platform.is_colliding:
                    border_color = (255, 255, 255)  # White border
                    # Draw a halo around the platform
                    halo_rect = rect.inflate(4, 4)
                    pygame.draw.rect(screen, (255, 255, 255), halo_rect)
                
                # Draw platform with a border
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, border_color, rect, 1)
                
                # Draw counter for disappearing platforms
                if isinstance(platform, DisappearingPlatform) and platform.jumps_remaining > 0:
                    font = pygame.font.SysFont(None, 20)
                    text = font.render(str(platform.jumps_remaining), True, (0, 0, 0))
                    screen.blit(text, (rect.centerx - text.get_width()//2, 
                                     rect.centery - text.get_height()//2))
    
    # For debugging
    def draw_platform_info(self, screen, camera_y):
        """Draw debug information about platforms"""
        # Draw total platform count
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"Platforms: {len(self.platforms)}", True, (0, 0, 0))
        screen.blit(text, (10, 40))
        
        # Draw highest and lowest platform info
        if self.platforms:
            highest_y = min([p.y for p in self.platforms])
            lowest_y = max([p.y for p in self.platforms])
            text1 = font.render(f"Highest: {highest_y:.0f} (screen: {highest_y - camera_y:.0f})", True, (0, 0, 0))
            text2 = font.render(f"Lowest: {lowest_y:.0f} (screen: {lowest_y - camera_y:.0f})", True, (0, 0, 0))
            screen.blit(text1, (10, 70))
            screen.blit(text2, (10, 100))
            
    def check_collision(self, player):
        # Check if player collides with any platform
        pass 