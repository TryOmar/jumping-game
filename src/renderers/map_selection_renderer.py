import pygame
from src.constants import WHITE, BLACK, GREEN, BLUE, YELLOW, RED

class MapSelectionRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
    
    def render_map_type_selection(self, game):
        """Render the map selection screen with Official and Custom map options"""
        # Background
        background_color = (70, 120, 170)  # Slightly different blue from main menu
        self.screen.fill(background_color)
        
        # Draw header
        header_font = pygame.font.SysFont(None, 56)
        header_text = header_font.render("SELECT MAP TYPE", True, WHITE)
        self.screen.blit(header_text, (self.width//2 - header_text.get_width()//2, 80))
        
        # Draw two main buttons: Official Maps and Custom Maps
        button_width, button_height = 300, 100
        padding = 40
        
        # Official Maps button
        official_rect = pygame.Rect(self.width//2 - button_width - padding//2, 200, button_width, button_height)
        pygame.draw.rect(self.screen, (40, 80, 120), official_rect)
        pygame.draw.rect(self.screen, WHITE, official_rect, 3)  # Button border
        
        official_font = pygame.font.SysFont(None, 36)
        official_text = official_font.render("OFFICIAL MAPS", True, WHITE)
        self.screen.blit(official_text, (official_rect.centerx - official_text.get_width()//2, 
                                      official_rect.centery - official_text.get_height()//2))
        
        # Custom Maps button
        custom_rect = pygame.Rect(self.width//2 + padding//2, 200, button_width, button_height)
        pygame.draw.rect(self.screen, (40, 80, 120), custom_rect)
        pygame.draw.rect(self.screen, WHITE, custom_rect, 3)  # Button border
        
        custom_font = pygame.font.SysFont(None, 36)
        custom_text = custom_font.render("CUSTOM MAPS", True, WHITE)
        self.screen.blit(custom_text, (custom_rect.centerx - custom_text.get_width()//2, 
                                    custom_rect.centery - custom_text.get_height()//2))
        
        # Add description text for each option
        desc_font = pygame.font.SysFont(None, 24)
        
        official_desc = "Pre-designed levels with progressive difficulty"
        official_desc_text = desc_font.render(official_desc, True, (220, 220, 220))
        self.screen.blit(official_desc_text, (official_rect.centerx - official_desc_text.get_width()//2, 
                                           official_rect.bottom + 10))
        
        custom_desc = "Create your own levels or play randomly generated maps"
        custom_desc_text = desc_font.render(custom_desc, True, (220, 220, 220))
        self.screen.blit(custom_desc_text, (custom_rect.centerx - custom_desc_text.get_width()//2, 
                                         custom_rect.bottom + 10))
        
        # Instructions
        instruction_font = pygame.font.SysFont(None, 24)
        instruction_text = instruction_font.render("Click on a map type to select, or press ESC to return", True, WHITE)
        self.screen.blit(instruction_text, (self.width//2 - instruction_text.get_width()//2, self.height - 40))
        
        # Store button rectangles in the game object for click detection
        game.map_selection_buttons = {
            "official": official_rect,
            "custom": custom_rect
        }
    
    def render_official_maps(self, game):
        """Render the official maps selection screen"""
        # Background
        background_color = (60, 110, 160)  # Slightly different blue
        self.screen.fill(background_color)
        
        # Draw header
        header_font = pygame.font.SysFont(None, 56)
        header_text = header_font.render("OFFICIAL MAPS", True, WHITE)
        self.screen.blit(header_text, (self.width//2 - header_text.get_width()//2, 80))
        
        # Small map previews
        map_preview_size = 120
        preview_y = 180
        map_spacing = 40
        
        # Available maps
        maps = [
            {"name": "Map 1", "x": self.width//2 - 230, "color": GREEN, "status": "Available", "key": "map1"},
            {"name": "Map 2", "x": self.width//2 - 80, "color": BLUE, "status": "Coming Soon"},
            {"name": "Map 3", "x": self.width//2 + 70, "color": YELLOW, "status": "Coming Soon"},
            {"name": "Map 4", "x": self.width//2 + 220, "color": RED, "status": "Coming Soon"}
        ]
        
        # Store button rectangles
        map_buttons = {}
        
        desc_font = pygame.font.SysFont(None, 24)
        
        for map_info in maps:
            map_rect = pygame.Rect(map_info["x"], preview_y, map_preview_size, map_preview_size)
            
            # Draw map preview
            pygame.draw.rect(self.screen, map_info["color"], map_rect)
            
            # Add gray overlay for unavailable maps
            if map_info["status"] == "Coming Soon":
                overlay = pygame.Surface((map_preview_size, map_preview_size), pygame.SRCALPHA)
                overlay.fill((100, 100, 100, 150))  # Semi-transparent gray
                self.screen.blit(overlay, map_rect)
            
            pygame.draw.rect(self.screen, WHITE, map_rect, 2)
            
            # Map name
            map_text = desc_font.render(map_info["name"], True, WHITE)
            self.screen.blit(map_text, (map_rect.centerx - map_text.get_width()//2, 
                                     map_rect.centery - map_text.get_height()//2))
            
            # Map status
            status_text = desc_font.render(map_info["status"], True, 
                                        (255, 255, 255) if map_info["status"] == "Available" else (255, 200, 0))
            self.screen.blit(status_text, (map_rect.centerx - status_text.get_width()//2, 
                                        map_rect.bottom + 10))
            
            # Store rect for available maps
            if map_info["status"] == "Available" and "key" in map_info:
                map_buttons[map_info["key"]] = map_rect
        
        # Map descriptions
        description_y = preview_y + map_preview_size + 60
        
        # Descriptions for each map
        descriptions = [
            "Basic level with standard platforms. Perfect for beginners!",
            "Faster platforms and moving obstacles. Test your reflexes!",
            "Challenging level with disappearing platforms. Timing is key!",
            "Ultimate challenge with all platform types and obstacles!"
        ]
        
        # Display description for selected map (or first map by default)
        selected_map = 0  # Default to the first map
        
        desc_text = descriptions[selected_map]
        desc_rendered = desc_font.render(desc_text, True, WHITE)
        self.screen.blit(desc_rendered, (self.width//2 - desc_rendered.get_width()//2, description_y))
        
        # Additional info for selected map
        info_y = description_y + 40
        
        # Add level info
        difficulty_labels = ["Easy", "Medium", "Hard", "Expert"]
        difficulty_text = desc_font.render(f"Difficulty: {difficulty_labels[selected_map]}", True, WHITE)
        self.screen.blit(difficulty_text, (self.width//2 - difficulty_text.get_width()//2, info_y))
        
        # Instructions
        instruction_font = pygame.font.SysFont(None, 24)
        instruction_text = instruction_font.render("Click on a map to select, or press ESC to return", True, WHITE)
        self.screen.blit(instruction_text, (self.width//2 - instruction_text.get_width()//2, self.height - 40))
        
        # Store button rectangles in the game object for click detection
        game.official_map_buttons = map_buttons
        
    def render_custom_maps(self, game):
        """Render the custom maps coming soon screen"""
        # Background
        background_color = (50, 70, 120)  # Darker blue
        self.screen.fill(background_color)
        
        # Draw header
        header_font = pygame.font.SysFont(None, 64)
        header_text = header_font.render("CUSTOM MAPS", True, WHITE)
        self.screen.blit(header_text, (self.width//2 - header_text.get_width()//2, 150))
        
        # Draw coming soon message
        message_font = pygame.font.SysFont(None, 36)
        message_text = message_font.render("The custom maps feature is coming soon!", True, (255, 220, 100))
        self.screen.blit(message_text, (self.width//2 - message_text.get_width()//2, 250))
        
        # Draw decorative elements
        pygame.draw.rect(self.screen, (80, 100, 150), (self.width//2 - 150, 320, 300, 5))
        
        # Draw instruction
        instruction_font = pygame.font.SysFont(None, 24)
        instruction_text = instruction_font.render("Press ESC to return", True, WHITE)
        self.screen.blit(instruction_text, (self.width//2 - instruction_text.get_width()//2, 400))
        
        # Draw animated construction icon or similar
        current_time = pygame.time.get_ticks()
        animation_frame = (current_time // 500) % 3  # Simple 3-frame animation
        
        # Draw some animated element based on the frame
        for i in range(3):
            color = YELLOW if i == animation_frame else (100, 100, 100)
            pygame.draw.rect(self.screen, color, (self.width//2 - 40 + i*30, 350, 20, 20)) 