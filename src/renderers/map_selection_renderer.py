import pygame
from src.constants import WHITE, BLACK, GREEN, BLUE, YELLOW, RED
from src.ui_styles import COLORS, FONT_SIZES, DIMENSIONS, create_centered_text, create_button

class MapSelectionRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
    
        # Define map configurations for reuse and maintainability
        self.map_configs = {
            "map1": {
                "name": "Map 1 - Beginner",
                "color": GREEN,
                "difficulty": "Easy",
                "description": "Basic level, mostly regular platforms. Good for beginners!",
                "config": {
                    "gravity": 0.7,
                    "player_speed": 3,
                    "jump_strength": 18,
                    "platform_density": 1.5,
                    "moving_platform_pct": 10,
                    "disappearing_platform_pct": 5,
                    "dangerous_platform_pct": 5
                }
            },
            "map2": {
                "name": "Map 2 - Explorer",
                "color": BLUE,
                "difficulty": "Medium",
                "description": "Faster platforms and more movement. Test your timing!",
                "config": {
                    "gravity": 0.6,
                    "player_speed": 4,
                    "jump_strength": 16,
                    "platform_density": 1.8,
                    "moving_platform_pct": 15,
                    "disappearing_platform_pct": 10,
                    "dangerous_platform_pct": 7
                }
            },
            "map3": {
                "name": "Map 3 - Challenger",
                "color": YELLOW,
                "difficulty": "Medium",
                "description": "More special platforms. Skill and precision required!",
                "config": {
                    "gravity": 0.2,
                    "player_speed": 5,
                    "jump_strength": 14,
                    "platform_density": 2.2,
                    "moving_platform_pct": 20,
                    "disappearing_platform_pct": 15,
                    "dangerous_platform_pct": 12
                }
            },
            "map4": {
                "name": "Map 4 - Master",
                "color": RED,
                "difficulty": "Hard",
                "description": "Ultimate challenge with all platform types. Experts only!",
                "config": {
                    "gravity": 0.4,
                    "player_speed": 6,
                    "jump_strength": 14,
                    "platform_density": 2.5,
                    "moving_platform_pct": 25,
                    "disappearing_platform_pct": 20,
                    "dangerous_platform_pct": 15
                }
            }
        }
    
    def render_map_type_selection(self, game):
        """Render the map selection screen with Official and Custom map options"""
        # Background
        self.screen.fill(COLORS["BG_MAP_SELECTION"])
        
        # Draw header with subtle shadow for depth
        create_centered_text(
            self.screen,
            "SELECT MAP TYPE",
            FONT_SIZES["HEADER"],
            COLORS["TEXT_WHITE"],
            80
        )
        
        # Add decorative underline for consistency with other screens
        pygame.draw.rect(
            self.screen, 
            COLORS["TEXT_WHITE"], 
            (self.width//2 - 180, 135, 360, 3)
        )
        
        # Draw two main buttons: Official Maps and Custom Maps with improved styling
        button_width = DIMENSIONS["BUTTON_WIDTH"]
        button_height = DIMENSIONS["BUTTON_HEIGHT"]
        padding = DIMENSIONS["BUTTON_PADDING"]
        button_y = 200
        
        # Official Maps button with subtle shadow for depth
        official_x = self.width//2 - button_width - padding//2
        official_rect = pygame.Rect(official_x, button_y, button_width, button_height)
        
        # Draw shadow
        shadow_rect = pygame.Rect(official_x + 5, button_y + 5, button_width, button_height)
        pygame.draw.rect(self.screen, (30, 60, 90), shadow_rect)
        
        # Draw main button
        create_button(
            self.screen, 
            "OFFICIAL MAPS", 
            official_rect,
            bg_color=COLORS["BUTTON_BLUE"],
            border_color=COLORS["TEXT_WHITE"],
            text_color=COLORS["TEXT_WHITE"],
            font_size=FONT_SIZES["MENU_OPTION"]
        )
        
        # Custom Maps button with subtle shadow for depth
        custom_x = self.width//2 + padding//2
        custom_rect = pygame.Rect(custom_x, button_y, button_width, button_height)
        
        # Draw shadow
        shadow_rect = pygame.Rect(custom_x + 5, button_y + 5, button_width, button_height)
        pygame.draw.rect(self.screen, (30, 60, 90), shadow_rect)
        
        # Draw main button
        create_button(
            self.screen, 
            "CUSTOM MAPS", 
            custom_rect,
            bg_color=COLORS["BUTTON_BLUE"],
            border_color=COLORS["TEXT_WHITE"],
            text_color=COLORS["TEXT_WHITE"],
            font_size=FONT_SIZES["MENU_OPTION"]
        )
        
        # Add description text for each option - fixed alignment
        desc_font = pygame.font.SysFont(None, FONT_SIZES["SMALL_TEXT"])
        
        # Create background areas for descriptions to improve readability
        desc_padding = 10
        desc_height = 30
        
        # Official maps description
        official_desc = "Pre-designed levels with progressive difficulty"
        official_desc_text = desc_font.render(official_desc, True, COLORS["DESCRIPTION_TEXT"])
        official_desc_width = official_desc_text.get_width() + desc_padding * 2
        
        official_desc_bg = pygame.Rect(
            official_rect.centerx - official_desc_width//2,
            official_rect.bottom + 10, 
            official_desc_width, 
            desc_height
        )
        pygame.draw.rect(self.screen, (40, 80, 120, 128), official_desc_bg, 0, 5)
        
        self.screen.blit(
            official_desc_text, 
            (official_rect.centerx - official_desc_text.get_width()//2, official_rect.bottom + 15)
        )
        
        # Custom maps description
        custom_desc = "Create your own levels or play randomly generated maps"
        custom_desc_text = desc_font.render(custom_desc, True, COLORS["DESCRIPTION_TEXT"])
        custom_desc_width = custom_desc_text.get_width() + desc_padding * 2
        
        custom_desc_bg = pygame.Rect(
            custom_rect.centerx - custom_desc_width//2,
            custom_rect.bottom + 10, 
            custom_desc_width, 
            desc_height
        )
        pygame.draw.rect(self.screen, (40, 80, 120, 128), custom_desc_bg, 0, 5)
        
        self.screen.blit(
            custom_desc_text, 
            (custom_rect.centerx - custom_desc_text.get_width()//2, custom_rect.bottom + 15)
        )
        
        # Instructions with improved styling
        instruction_text = "Click on a map type to select, or press ESC to return"
        create_centered_text(
            self.screen,
            instruction_text,
            FONT_SIZES["FOOTER_NOTE"],
            COLORS["TEXT_WHITE"],
            self.height - 40
        )
        
        # Store button rectangles in the game object for click detection
        game.map_selection_buttons = {
            "official": official_rect,
            "custom": custom_rect
        }
    
    def render_official_maps(self, game):
        """Render the official maps selection screen with 4 available maps"""
        # Background
        self.screen.fill(COLORS["BG_OFFICIAL_MAPS"])
        
        # Draw header with decorative underline for consistency
        create_centered_text(
            self.screen,
            "OFFICIAL MAPS",
            FONT_SIZES["HEADER"] - 4,  # Slightly smaller header
            COLORS["TEXT_WHITE"],
            75
        )
        
        # Draw decorative line under header
        pygame.draw.rect(
            self.screen,
            COLORS["TEXT_WHITE"],
            (self.width//2 - 180, 125, 360, 3)
        )
        
        # Initialize selected map if not already set
        if not hasattr(game, 'selected_official_map'):
            game.selected_official_map = "map1"
        
        # Map preview size and positioning - adjusted for better spacing
        map_preview_size = 85
        preview_y = 165
        margin = 45
        total_width = (map_preview_size * 4) + (margin * 3)
        start_x = (self.width - total_width) // 2
        
        # Available maps with calculated x positions
        maps = [
            {"key": "map1", "x": start_x},
            {"key": "map2", "x": start_x + map_preview_size + margin},
            {"key": "map3", "x": start_x + (map_preview_size + margin) * 2},
            {"key": "map4", "x": start_x + (map_preview_size + margin) * 3}
        ]
        
        # Store button rectangles
        map_buttons = {}
        
        # Common fonts - smaller for better fit
        title_font = pygame.font.SysFont(None, FONT_SIZES["SMALL_TEXT"] - 2)
        diff_font = pygame.font.SysFont(None, FONT_SIZES["SMALL_TEXT"] - 6)
        
        # Draw map previews with selection indicator
        for map_info in maps:
            map_key = map_info["key"]
            map_data = self.map_configs[map_key]
            map_rect = pygame.Rect(map_info["x"], preview_y, map_preview_size, map_preview_size)
            
            # Draw map preview shadow for depth
            shadow_rect = pygame.Rect(map_info["x"] + 2, preview_y + 2, map_preview_size, map_preview_size)
            pygame.draw.rect(self.screen, (25, 50, 75), shadow_rect, 0, 4)
            
            # Draw map preview
            pygame.draw.rect(self.screen, map_data["color"], map_rect, 0, 4)
            
            # Draw selection indicator if this map is selected
            if game.selected_official_map == map_key:
                pygame.draw.rect(self.screen, WHITE, map_rect, 3, 4)
                triangle_size = 8
                pygame.draw.polygon(self.screen, WHITE, [
                    (map_rect.left + 2, map_rect.top + 2),
                    (map_rect.left + triangle_size + 2, map_rect.top + 2),
                    (map_rect.left + 2, map_rect.top + triangle_size + 2)
                ])
                pygame.draw.polygon(self.screen, WHITE, [
                    (map_rect.right - 2, map_rect.bottom - 2),
                    (map_rect.right - triangle_size - 2, map_rect.bottom - 2),
                    (map_rect.right - 2, map_rect.bottom - triangle_size - 2)
                ])
            else:
                pygame.draw.rect(self.screen, WHITE, map_rect, 1, 4)
            
            # Improved map name display with proper sizing
            simple_name = f"Map {map_key[-1]}"
            name_text = title_font.render(simple_name, True, WHITE)
            name_width = name_text.get_width()
            
            # Create a darker background for text that fits the width of the text
            name_bg_rect = pygame.Rect(map_rect.centerx - name_width//2 - 4, map_rect.top + 4, name_width + 8, name_text.get_height() + 4)
            pygame.draw.rect(self.screen, (0, 0, 0, 180), name_bg_rect, 0, 3)
            
            # Draw name centered on the map
            self.screen.blit(name_text, (map_rect.centerx - name_width//2, map_rect.top + 6))
            
            # Difficulty label with improved visuals
            difficulty_colors = {
                "Easy": (120, 255, 120),
                "Medium": (255, 255, 120),
                "Hard": (255, 120, 120)
            }
            
            # Simplified difficulty display
            diff_text_str = map_data['difficulty']
            diff_render = diff_font.render(diff_text_str, True, difficulty_colors.get(diff_text_str, WHITE))
            diff_width = diff_render.get_width()
            
            # Background for difficulty that fits properly
            diff_bg_rect = pygame.Rect(map_rect.centerx - diff_width//2 - 4, map_rect.bottom - diff_render.get_height() - 8, diff_width + 8, diff_render.get_height() + 4)
            pygame.draw.rect(self.screen, (0, 0, 0, 180), diff_bg_rect, 0, 3)
            
            # Draw difficulty text
            self.screen.blit(diff_render, (map_rect.centerx - diff_width//2, map_rect.bottom - diff_render.get_height() - 6))
            
            # Store rect for click detection - Make sure all maps are clickable
            map_buttons[map_key] = map_rect
        
        # Draw selected map details section - improved layout
        selected_data = self.map_configs[game.selected_official_map]
        details_y = preview_y + map_preview_size + 35
        
        # Create background panel for details
        details_panel = pygame.Rect(self.width//2 - 280, details_y, 560, 125)
        pygame.draw.rect(self.screen, (35, 65, 95, 220), details_panel, 0, 8)
        pygame.draw.rect(self.screen, WHITE, details_panel, 1, 8)
        
        # Map title
        map_title = f"{selected_data['name']} ({selected_data['difficulty']})"
        create_centered_text(
            self.screen,
            map_title,
            FONT_SIZES["STANDARD_TEXT"] - 6,
            WHITE,
            details_y + 15
        )
        
        # Map description
        create_centered_text(
            self.screen,
            selected_data['description'],
            FONT_SIZES["SMALL_TEXT"] - 4,
            COLORS["DESCRIPTION_TEXT"],
            details_y + 40
        )
        
        # Map stats in 2 columns with better spacing
        stats_y_base = details_y + 65
        stats_col1_x = self.width//2 - 220
        stats_col2_x = self.width//2 + 10
        
        # Draw faint separator line between columns
        pygame.draw.line(self.screen, (120, 120, 150, 100), 
                      (self.width//2 - 5, stats_y_base - 2), 
                      (self.width//2 - 5, stats_y_base + 48), 1)
        
        # Draw stats with labels
        stat_font = pygame.font.SysFont(None, FONT_SIZES["SMALL_TEXT"] - 4)
        value_font = pygame.font.SysFont(None, FONT_SIZES["SMALL_TEXT"] - 4)
        stats_line_height = 18
        
        stats_left = [
            {"label": "Gravity", "value": selected_data["config"]["gravity"], "format": "{:.1f}"},
            {"label": "Player Speed", "value": selected_data["config"]["player_speed"], "format": "{:.0f}"},
            {"label": "Jump Strength", "value": selected_data["config"]["jump_strength"], "format": "{:.0f}"}
        ]
        
        stats_right = [
            {"label": "Density", "value": selected_data["config"]["platform_density"], "format": "{:.1f}"},
            {"label": "Moving %", "value": selected_data["config"]["moving_platform_pct"], "format": "{:.0f}%"},
            {"label": "Dangerous %", "value": selected_data["config"]["dangerous_platform_pct"], "format": "{:.0f}%"}
        ]
        
        # Draw left column stats
        for i, stat in enumerate(stats_left):
            stat_y = stats_y_base + i * stats_line_height
            
            # Label
            label_text = stat_font.render(stat["label"] + ":", True, (180, 180, 255))
            self.screen.blit(label_text, (stats_col1_x, stat_y))
            
            # Value - aligned fixed position from label
            value_str = stat["format"].format(stat["value"])
            value_text = value_font.render(value_str, True, (240, 240, 140))
            self.screen.blit(value_text, (stats_col1_x + 100, stat_y))
        
        # Draw right column stats
        for i, stat in enumerate(stats_right):
            stat_y = stats_y_base + i * stats_line_height
            
            # Label
            label_text = stat_font.render(stat["label"] + ":", True, (180, 180, 255))
            self.screen.blit(label_text, (stats_col2_x, stat_y))
            
            # Value - aligned fixed position from label
            value_str = stat["format"].format(stat["value"])
            value_text = value_font.render(value_str, True, (240, 240, 140))
            self.screen.blit(value_text, (stats_col2_x + 100, stat_y))
        
        # Play selected map button with shadow for depth - moved higher
        play_button_y = details_y + 125 + 5
        play_button_width = 200
        play_button_height = 40
        play_button_x = self.width//2 - play_button_width//2
        
        # Draw shadow
        shadow_rect = pygame.Rect(play_button_x + 2, play_button_y + 2, play_button_width, play_button_height)
        pygame.draw.rect(self.screen, (25, 50, 75), shadow_rect, 0, 4)
        
        # Draw play button
        play_button_rect = pygame.Rect(play_button_x, play_button_y, play_button_width, play_button_height)
        create_button(
            self.screen, 
            f"PLAY MAP {selected_data['name'].split(' ')[1]}",
            play_button_rect,
            bg_color=(50, 110, 50),
            border_color=WHITE,
            text_color=WHITE,
            font_size=FONT_SIZES["STANDARD_TEXT"] - 10
        )
        
        # Add play button to buttons dict
        map_buttons["play"] = play_button_rect
        
        # Instructions with improved styling
        instruction_text = "Click a map to select. Press PLAY or ESC to return."
        create_centered_text(
            self.screen,
            instruction_text,
            FONT_SIZES["FOOTER_NOTE"] - 4,
            WHITE,
            self.height - 25
        )
        
        # Store button rectangles and map configs in the game object
        game.official_map_buttons = map_buttons
        game.official_map_configs = {key: self.map_configs[key]["config"] for key in self.map_configs}
        
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
        play_button_rect = pygame.Rect(self.width//2 - 150, play_button_y, 300, 50)
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
        instruction_y = reset_button_bottom + (space_below // 3)
        self.screen.blit(instruction_text, (self.width//2 - instruction_text.get_width()//2, instruction_y)) 