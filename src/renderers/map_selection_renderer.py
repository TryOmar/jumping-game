import pygame
from src.constants import WHITE, BLACK, GREEN, BLUE, YELLOW, RED
from src.ui_styles import COLORS, FONT_SIZES, DIMENSIONS, create_centered_text, create_button

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
        """Render the custom maps configuration screen"""
        # Background
        self.screen.fill(COLORS["BG_CUSTOM_MAPS"])
        
        # Draw header
        create_centered_text(
            self.screen,
            "CUSTOM MAP SETTINGS",
            FONT_SIZES["HEADER"],
            COLORS["TEXT_WHITE"],
            60
        )
        
        # Draw decorative line under header
        pygame.draw.rect(
            self.screen,
            COLORS["TEXT_WHITE"],
            (self.width//2 - 180, 110, 360, 3)
        )
        
        # Initialize settings if not already done
        if not hasattr(game, 'custom_map_settings'):
            game.custom_map_settings = {
                "gravity": 0.5,
                "player_speed": 5,
                "jump_strength": 10,
                "platform_density": 2.0,
                "moving_platform_pct": 25,
                "disappearing_platform_pct": 15,
                "dangerous_platform_pct": 10,
                "active_setting": None  # Track which setting is being edited
            }
        
        # Common fonts
        label_font = pygame.font.SysFont(None, FONT_SIZES["STANDARD_TEXT"])
        value_font = pygame.font.SysFont(None, FONT_SIZES["STANDARD_TEXT"])
        
        # Layout settings
        settings_start_y = 160
        setting_height = 50
        
        # Position settings (similar to settings screen)
        left_margin = 80
        right_margin = self.width - 300
        slider_width = 200
        
        # Settings and their ranges
        settings = [
            {"name": "Gravity", "key": "gravity", "min": 0.1, "max": 1.0, "step": 0.1, "format": "{:.1f}"},
            {"name": "Player Speed", "key": "player_speed", "min": 3, "max": 8, "step": 1, "format": "{:.0f}"},
            {"name": "Jump Strength", "key": "jump_strength", "min": 8, "max": 15, "step": 1, "format": "{:.0f}"},
            {"name": "Platform Density", "key": "platform_density", "min": 1.0, "max": 3.0, "step": 0.5, "format": "{:.1f}"},
            {"name": "Moving Platforms %", "key": "moving_platform_pct", "min": 0, "max": 50, "step": 5, "format": "{:.0f}%"},
            {"name": "Disappearing Platforms %", "key": "disappearing_platform_pct", "min": 0, "max": 30, "step": 5, "format": "{:.0f}%"},
            {"name": "Dangerous Platforms %", "key": "dangerous_platform_pct", "min": 0, "max": 20, "step": 5, "format": "{:.0f}%"}
        ]
        
        # Track slider rectangles for interaction
        game.custom_map_sliders = {}
        game.custom_map_buttons = {}
        
        # Draw each setting with label, slider, and value
        for i, setting in enumerate(settings):
            current_y = settings_start_y + i * setting_height
            
            # Label
            label_text = label_font.render(setting["name"], True, COLORS["TEXT_WHITE"])
            self.screen.blit(label_text, (left_margin, current_y + label_text.get_height()//2))
            
            # Get current value
            current_value = game.custom_map_settings[setting["key"]]
            
            # Calculate slider position
            slider_left = right_margin
            slider_top = current_y + 7
            slider_height = 10
            
            # Calculate normalized position (0-1) based on min/max
            value_range = setting["max"] - setting["min"]
            normalized_pos = (current_value - setting["min"]) / value_range
            
            # Draw slider background
            slider_bg_rect = pygame.Rect(slider_left, slider_top, slider_width, slider_height)
            pygame.draw.rect(self.screen, (100, 100, 100), slider_bg_rect)
            
            # Draw slider fill
            fill_width = int(normalized_pos * slider_width)
            slider_fill_rect = pygame.Rect(slider_left, slider_top, fill_width, slider_height)
            pygame.draw.rect(self.screen, COLORS["BUTTON_BLUE"], slider_fill_rect)
            
            # Draw slider handle
            handle_size = 20
            handle_x = slider_left + fill_width - handle_size//2
            handle_y = slider_top + slider_height//2 - handle_size//2
            handle_rect = pygame.Rect(handle_x, handle_y, handle_size, handle_size)
            pygame.draw.rect(self.screen, COLORS["TEXT_WHITE"], handle_rect)
            
            # Store slider rect for interaction
            game.custom_map_sliders[setting["key"]] = {
                "rect": pygame.Rect(slider_left, slider_top - 10, slider_width, slider_height + 20),
                "min": setting["min"],
                "max": setting["max"],
                "step": setting["step"],
                "format": setting["format"]
            }
            
            # Value text
            format_string = setting["format"]
            if "%" in format_string:
                value_str = format_string.format(current_value)
            else:
                value_str = format_string.format(current_value)
                
            value_text = value_font.render(value_str, True, COLORS["SETTING_VALUE"])
            self.screen.blit(value_text, (slider_left + slider_width + 20, current_y + value_text.get_height()//2))
        
        # Play button
        play_button_y = settings_start_y + len(settings) * setting_height + 40
        play_button_rect = pygame.Rect(self.width//2 - 150, play_button_y, 300, 50)  # Wider button (300px instead of 200px)
        create_button(
            self.screen, 
            "PLAY CUSTOM MAP", 
            play_button_rect,
            bg_color=COLORS["BUTTON_BLUE"],
            border_color=COLORS["TEXT_WHITE"],
            text_color=COLORS["TEXT_WHITE"]
        )
        game.custom_map_buttons["play"] = play_button_rect
        
        # Reset button
        reset_button_rect = pygame.Rect(self.width//2 - 100, play_button_y + 70, 200, 40)
        create_button(
            self.screen, 
            "Reset to Default", 
            reset_button_rect,
            bg_color=(80, 80, 80),
            border_color=COLORS["TEXT_WHITE"],
            text_color=COLORS["TEXT_WHITE"],
            font_size=FONT_SIZES["SMALL_TEXT"]
        )
        game.custom_map_buttons["reset"] = reset_button_rect
        
        # Instructions - moved much higher above the buttons
        instruction_font = pygame.font.SysFont(None, FONT_SIZES["FOOTER_NOTE"])
        instruction_text = instruction_font.render("Drag sliders to adjust settings, then click PLAY", True, COLORS["TEXT_WHITE"])
        # Position between the reset button and the bottom of the screen
        reset_button_bottom = reset_button_rect.bottom
        space_below = self.height - reset_button_bottom
        instruction_y = reset_button_bottom + (space_below // 3)  # Position 1/3 of the way between reset button and bottom
        self.screen.blit(instruction_text, (self.width//2 - instruction_text.get_width()//2, instruction_y)) 