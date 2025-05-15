import pygame
import random
from src.platform import Platform, MovingPlatform, DisappearingPlatform, DangerousPlatform
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLATFORM_COUNT, WHITE, BLACK, RED, GREEN, BLUE, PLATFORM_COLORS, PLATFORM_WIDTH, PLATFORM_HEIGHT

class Map:
    def __init__(self, theme_color=(0, 150, 0), gravity=0.5, platform_speed=2):
        self.platforms = []
        self.theme_color = theme_color
        self.gravity = gravity
        self.platform_speed = platform_speed
        self.target_height = -5000  # Negative because we'll be going up
        self.debug_mode = False
        
    def generate_map(self):
        """Generate the initial platforms for the map"""
        # Clear any existing platforms
        self.platforms = []
        
        # Create a starter platform at the bottom
        start_platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT)
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
                platform = Platform(x, y, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT)
            elif platform_type == "moving":
                platform = MovingPlatform(x, y, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT, speed=self.platform_speed)
            elif platform_type == "disappearing":
                platform = DisappearingPlatform(x, y, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT)
            elif platform_type == "dangerous":
                platform = DangerousPlatform(x, y, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT)
            
            self.platforms.append(platform)
        
    def update(self, camera_y):
        """Update all platforms, remove off-screen ones, generate new ones"""
        # Update platforms based on type
        for platform in self.platforms:
            platform.update(camera_y)
            
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
        platform_count = 10  # Generate more platforms at once for better coverage
        
        # Debug print
        if self.debug_mode:
            print(f"Generating new platforms. Camera Y: {camera_y}, Highest platform Y: {highest_y}")
        
        for i in range(platform_count):
            # Position each new platform above the highest one with fixed gap
            # Make sure platforms are generated in world coordinates
            y = highest_y - (i + 1) * vertical_gap
            
            # Ensure we're generating platforms in a good pattern for gameplay
            # Alternate between left, center, and right sections of the screen
            section = i % 3  # 0, 1, or 2
            
            if section == 0:  # Left section
                x = random.randint(50, SCREEN_WIDTH // 3 - 50)
            elif section == 1:  # Center section
                x = random.randint(SCREEN_WIDTH // 3 + 50, 2 * SCREEN_WIDTH // 3 - 50)
            else:  # Right section
                x = random.randint(2 * SCREEN_WIDTH // 3 + 50, SCREEN_WIDTH - 150)
            
            # Randomize platform type with weights
            platform_type = random.choices(
                ["regular", "moving", "disappearing", "dangerous"],
                weights=[0.7, 0.15, 0.1, 0.05],  # More regular platforms for better gameplay
                k=1
            )[0]
            
            # Create platform with consistent width
            platform_width = random.randint(80, 120)  # Vary width slightly
            
            # Create the appropriate platform type
            if platform_type == "regular":
                platform = Platform(x, y, width=platform_width, height=PLATFORM_HEIGHT)
            elif platform_type == "moving":
                platform = MovingPlatform(x, y, width=platform_width, height=PLATFORM_HEIGHT, speed=self.platform_speed)
            elif platform_type == "disappearing":
                platform = DisappearingPlatform(x, y, width=platform_width, height=PLATFORM_HEIGHT)
            elif platform_type == "dangerous":
                platform = DangerousPlatform(x, y, width=platform_width, height=PLATFORM_HEIGHT)
            
            # Ensure platforms don't overlap (simple check)
            overlapping = False
            for existing_platform in self.platforms:
                if (abs(existing_platform.y - y) < PLATFORM_HEIGHT * 2 and 
                    abs(existing_platform.x - x) < platform_width):
                    overlapping = True
                    break
            
            if not overlapping:
                self.platforms.append(platform)
            
    def draw(self, screen, camera_y):
        """Draw the map"""
        # Draw platforms
        for platform in self.platforms:
            # Calculate screen position - THIS IS KEY:
            # Platform.y is in world coordinates, we need to convert to screen coordinates
            # by subtracting the camera position
            screen_y = platform.y - camera_y
            
            # Only draw platforms that are visible on screen
            # Add more margin so platforms appear earlier when scrolling upward
            if screen_y > -platform.height * 4 and screen_y < screen.get_height() + platform.height * 2:
                # Create rectangle for drawing
                rect = pygame.Rect(platform.x, screen_y, platform.width, platform.height)
                
                # Choose platform color
                color = platform.color
                
                # Draw the platform
                pygame.draw.rect(screen, color, rect)
                
                # Draw border around platform (helps see exact collision area)
                border_color = BLACK
                if platform.colliding and self.debug_mode:
                    border_color = RED  # Red border for colliding platforms in debug mode
                    # Draw a highlight effect for better visibility
                    highlight_rect = rect.inflate(4, 4)
                    pygame.draw.rect(screen, (255, 255, 255), highlight_rect, 1)
                pygame.draw.rect(screen, border_color, rect, 2)
                
                # For disappearing platforms, show jumps remaining
                if isinstance(platform, DisappearingPlatform) and platform.jumps_remaining > 0:
                    font = pygame.font.SysFont(None, 18)
                    text = font.render(str(platform.jumps_remaining), True, BLACK)
                    screen.blit(text, (rect.centerx - text.get_width()//2, 
                                      rect.centery - text.get_height()//2))
                
                # In debug mode, show platform id and position
                if self.debug_mode:
                    font = pygame.font.SysFont(None, 18)
                    # Show world and screen coordinates
                    text = font.render(f"ID:{platform.id}", True, BLACK)
                    screen.blit(text, (platform.x + 5, screen_y + 5))
    
    def draw_platform_info(self, screen, camera_y):
        """Draw detailed platform info in debug mode"""
        font = pygame.font.SysFont(None, 14)
        y_pos = 250  # Starting y position
        
        # Draw total platform count
        count_font = pygame.font.SysFont(None, 18)
        count_text = count_font.render(f"Total Platforms: {len(self.platforms)}", True, BLACK)
        screen.blit(count_text, (10, 240))
        
        # Find the highest and lowest platforms
        if self.platforms:
            highest_y = min([p.y for p in self.platforms])
            lowest_y = max([p.y for p in self.platforms])
            
            highest_text = count_font.render(f"Highest: {highest_y:.0f} (screen: {highest_y - camera_y:.0f})", True, BLACK)
            lowest_text = count_font.render(f"Lowest: {lowest_y:.0f} (screen: {lowest_y - camera_y:.0f})", True, BLACK)
            
            screen.blit(highest_text, (10, 260))
            screen.blit(lowest_text, (10, 280))
        
        for i, platform in enumerate(self.platforms):
            # Only show info for visible or nearly visible platforms
            screen_y = platform.y - camera_y
            if screen_y > -platform.height * 3 and screen_y < screen.get_height() + platform.height * 2:
                # Format: ID (World X,Y) → (Screen X,Y)
                info_text = f"Platform {platform.id}: ({platform.x:.0f},{platform.y:.0f}) → ({platform.x:.0f},{screen_y:.0f})"
                if platform.colliding:
                    info_text += " [COLLIDING]"
                    
                text = font.render(info_text, True, BLACK)
                screen.blit(text, (10, y_pos + 40))
                y_pos += 20
                
                # Limit number of platform info to display
                if i >= 10:  # Only show 10 platforms max
                    remaining = len(self.platforms) - i - 1
                    more_text = font.render(f"...and {remaining} more platforms", True, BLACK)
                    screen.blit(more_text, (10, y_pos + 40))
                    break
    
    def check_collision(self, player):
        # Check if player collides with any platform
        pass 