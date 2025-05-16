import pygame
import random
from src.platform import Platform, MovingPlatform, DisappearingPlatform, DangerousPlatform
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLATFORM_COUNT, WHITE, BLACK, RED, GREEN, BLUE, PLATFORM_COLORS, PLATFORM_WIDTH, PLATFORM_HEIGHT

class Map:
    def __init__(self, theme_color=(0, 150, 0), gravity=0.5, platform_speed=2, platform_density=2.0, 
                 moving_platform_pct=25, disappearing_platform_pct=15, dangerous_platform_pct=10):
        self.platforms = []
        self.theme_color = theme_color
        self.gravity = gravity
        self.platform_speed = platform_speed
        self.target_height = -5000  # Negative because we'll be going up
        self.debug_mode = False
        self.game = None  # Reference to game object for sound effects
        
        # Custom platform generation settings
        self.platform_density = platform_density  # Higher = more platforms (closer together)
        self.moving_platform_pct = moving_platform_pct / 100.0  # Convert to decimal
        self.disappearing_platform_pct = disappearing_platform_pct / 100.0
        self.dangerous_platform_pct = dangerous_platform_pct / 100.0
        
        # Calculate regular platform percentage based on others
        total_special = self.moving_platform_pct + self.disappearing_platform_pct + self.dangerous_platform_pct
        self.regular_platform_pct = max(0, 1.0 - total_special)
        
    def set_game(self, game):
        """Set reference to game object for sound effects"""
        self.game = game
        
        # Set game reference on all existing platforms
        for platform in self.platforms:
            if isinstance(platform, MovingPlatform):
                platform.set_game(game)
        
    def generate_map(self):
        """Generate the initial platforms for the map"""
        # Clear any existing platforms
        self.platforms = []
        
        # Create a starter platform at the bottom
        start_platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT)
        self.platforms.append(start_platform)
        
        # Calculate vertical gap based on platform density
        # Higher density = smaller gap
        base_gap = 70  # Default gap
        vertical_gap = int(base_gap / self.platform_density)
        vertical_gap = max(40, min(100, vertical_gap))  # Constrain between 40-100
        
        # Generate initial platforms going upward with density-based spacing
        for i in range(PLATFORM_COUNT):
            # Calculate y position with density-adjusted spacing
            y = SCREEN_HEIGHT - 100 - i * vertical_gap
            
            # Ensure good horizontal distribution
            # Divide screen into sections for better distribution
            section_width = SCREEN_WIDTH // 3
            section = i % 3  # 0, 1, or 2
            
            # Random x within the section to ensure platforms across the screen
            min_x = section * section_width + 20
            max_x = (section + 1) * section_width - 120
            x = random.randint(min_x, max_x)
            
            # Create platform with the configured probabilities
            platform = self._create_platform_by_type(x, y)
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
    
    def _create_platform_by_type(self, x, y, width=PLATFORM_WIDTH):
        """Create a platform based on configured percentages"""
        # Randomize platform type based on configured percentages
        platform_type = random.choices(
            ["regular", "moving", "disappearing", "dangerous"],
            weights=[
                self.regular_platform_pct, 
                self.moving_platform_pct,
                self.disappearing_platform_pct,
                self.dangerous_platform_pct
            ],
            k=1
        )[0]
        
        # Create the appropriate platform type
        if platform_type == "regular":
            return Platform(x, y, width=width, height=PLATFORM_HEIGHT)
        elif platform_type == "moving":
            platform = MovingPlatform(x, y, width=width, height=PLATFORM_HEIGHT, speed=self.platform_speed)
            if self.game:
                platform.set_game(self.game)
            return platform
        elif platform_type == "disappearing":
            return DisappearingPlatform(x, y, width=width, height=PLATFORM_HEIGHT)
        elif platform_type == "dangerous":
            return DangerousPlatform(x, y, width=width, height=PLATFORM_HEIGHT)
    
    def generate_more_platforms(self, camera_y):
        """Generate additional platforms as the player moves up"""
        # Find the highest platform
        highest_y = min([p.y for p in self.platforms]) if self.platforms else SCREEN_HEIGHT
        
        # Calculate vertical gap based on platform density
        base_gap = 70  # Default gap
        vertical_gap = int(base_gap / self.platform_density)
        vertical_gap = max(40, min(100, vertical_gap))  # Constrain between 40-100
        
        # Generate more platforms with density-adjusted spacing
        platform_count = 10  # Generate more platforms at once for better coverage
        
        # Debug print
        if self.debug_mode:
            print(f"Generating new platforms. Camera Y: {camera_y}, Highest platform Y: {highest_y}")
        
        for i in range(platform_count):
            # Position each new platform above the highest one with configured gap
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
            
            # Create platform with consistent width
            platform_width = random.randint(80, 120)  # Vary width slightly
            
            # Create platform using helper method
            platform = self._create_platform_by_type(x, y, platform_width)
            
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
            
            # Also show platform distribution
            platform_types = {
                "regular": 0,
                "moving": 0,
                "disappearing": 0,
                "dangerous": 0
            }
            
            for platform in self.platforms:
                if isinstance(platform, MovingPlatform):
                    platform_types["moving"] += 1
                elif isinstance(platform, DisappearingPlatform):
                    platform_types["disappearing"] += 1
                elif isinstance(platform, DangerousPlatform):
                    platform_types["dangerous"] += 1
                else:
                    platform_types["regular"] += 1
            
            # Display counts
            dist_y = 300
            for p_type, count in platform_types.items():
                dist_text = count_font.render(f"{p_type.capitalize()}: {count}", True, BLACK)
                screen.blit(dist_text, (10, dist_y))
                dist_y += 20
    
    def check_collision(self, player):
        # Check if player collides with any platform
        for platform in self.platforms:
            if platform.check_collision(player):
                return platform
        return None 