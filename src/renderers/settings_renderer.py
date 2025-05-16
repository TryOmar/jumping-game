import pygame
from src.constants import WHITE, BLACK
from src.config.settings import get_setting, update_setting
from src.ui_styles import COLORS, FONT_SIZES, DIMENSIONS, create_centered_text, create_button


class SettingsRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Available resolutions
        self.resolutions = [
            (800, 600), (1024, 768), (1280, 720), 
            (1366, 768), (1920, 1080)
        ]
        
        # Current resolution index - get from settings or default
        current_w, current_h = get_setting("WINDOW", "width", self.width), get_setting("WINDOW", "height", self.height)
        self.current_resolution_idx = 0
        for i, res in enumerate(self.resolutions):
            if res == (current_w, current_h):
                self.current_resolution_idx = i
                break
        
        # Fullscreen state - get from settings
        self.fullscreen_enabled = get_setting("WINDOW", "fullscreen", False)

        # Slider dimensions
        self.slider_width = 200
        self.slider_height = 20
        
        # Layout positions
        self.left_margin = 150 # Adjusted for more space
        self.right_margin_controls = self.width - self.left_margin - self.slider_width # Controls aligned to the right of labels
        self.value_right_margin = self.width - 150 # For text values like ON/OFF

        # Clickable rects for resolution arrows and fullscreen toggle
        self.res_left_arrow_rect = None
        self.res_right_arrow_rect = None
        self.fullscreen_toggle_rect = None
        self.back_button_rect = None


    def render(self, game):
        """Render the settings screen"""
        # Store game reference for use in apply_settings
        self._game_ref = game
        
        self.screen.fill(COLORS.get("BG_SETTINGS", (60, 80, 140)))
        
        # Initialize game.settings_sliders and game.settings_buttons for EventHandler
        if not hasattr(game, 'settings_sliders'):
            game.settings_sliders = {}
        if not hasattr(game, 'settings_buttons'):
            game.settings_buttons = {}

        # Header
        header_font = pygame.font.SysFont(None, FONT_SIZES["TITLE_MEDIUM"]) # Larger header
        header_text = header_font.render("SETTINGS", True, COLORS["TEXT_WHITE"])
        header_x = self.width // 2 - header_text.get_width() // 2
        self.screen.blit(header_text, (header_x, 50)) # Adjusted Y

        option_font = pygame.font.SysFont(None, FONT_SIZES["MENU_OPTION"]) # Standardized font
        value_font = pygame.font.SysFont(None, FONT_SIZES["MENU_OPTION"])
        y_offset = 150 # Start Y for options

        # Resolution setting
        res_label_text = option_font.render("Resolution:", True, COLORS["TEXT_WHITE"])
        self.screen.blit(res_label_text, (self.left_margin, y_offset))
        
        current_res_tuple = self.resolutions[self.current_resolution_idx]
        res_value_str = f"{current_res_tuple[0]}x{current_res_tuple[1]}"
        res_value_surface = value_font.render(res_value_str, True, COLORS.get("SETTING_VALUE", (200, 255, 200)))
        
        # Resolution arrows and value text
        arrow_size = res_value_surface.get_height() // 2
        
        # Left Arrow
        self.res_left_arrow_rect = pygame.Rect(self.right_margin_controls - arrow_size - 5, y_offset + arrow_size // 2, arrow_size, arrow_size)
        pygame.draw.polygon(self.screen, COLORS["TEXT_WHITE"], [
            (self.res_left_arrow_rect.right, self.res_left_arrow_rect.top),
            (self.res_left_arrow_rect.left, self.res_left_arrow_rect.centery),
            (self.res_left_arrow_rect.right, self.res_left_arrow_rect.bottom)
        ])
        
        res_value_x = self.res_left_arrow_rect.right + 10
        self.screen.blit(res_value_surface, (res_value_x, y_offset))

        # Right Arrow
        self.res_right_arrow_rect = pygame.Rect(res_value_x + res_value_surface.get_width() + 10, y_offset + arrow_size // 2, arrow_size, arrow_size)
        pygame.draw.polygon(self.screen, COLORS["TEXT_WHITE"], [
            (self.res_right_arrow_rect.left, self.res_right_arrow_rect.top),
            (self.res_right_arrow_rect.right, self.res_right_arrow_rect.centery),
            (self.res_right_arrow_rect.left, self.res_right_arrow_rect.bottom)
        ])
        game.settings_buttons['res_left'] = self.res_left_arrow_rect
        game.settings_buttons['res_right'] = self.res_right_arrow_rect
        
        y_offset += 50

        # Fullscreen toggle
        fullscreen_label_text = option_font.render("Fullscreen:", True, COLORS["TEXT_WHITE"])
        self.screen.blit(fullscreen_label_text, (self.left_margin, y_offset))
        
        fullscreen_value_str = "ON" if self.fullscreen_enabled else "OFF"
        fs_color_key = "SUCCESS_GREEN" if self.fullscreen_enabled else "DANGER_RED"
        fullscreen_value_surface = value_font.render(fullscreen_value_str, True, COLORS.get(fs_color_key, COLORS["TEXT_WHITE"]))
        
        self.fullscreen_toggle_rect = fullscreen_value_surface.get_rect(topleft=(self.right_margin_controls, y_offset))
        self.screen.blit(fullscreen_value_surface, self.fullscreen_toggle_rect.topleft)
        game.settings_buttons['fullscreen_toggle'] = self.fullscreen_toggle_rect

        y_offset += 50

        # Volume Sliders (using game.audio_settings for values)
        slider_y_start = y_offset
        
        # Master Volume (Example, assuming it exists in game.audio_settings)
        # if 'master_volume' in game.audio_settings:
        #     self._render_slider(game, "master_volume", "Master Volume", slider_y_start, option_font, value_font)
        #     slider_y_start += 50

        self._render_slider(game, "sfx_volume", "Sound Volume", slider_y_start, option_font, value_font)
        slider_y_start += 50
        self._render_slider(game, "music_volume", "Music Volume", slider_y_start, option_font, value_font)
        
        y_offset = slider_y_start + 50


        # Back Button
        button_width, button_height = 200, 50
        self.back_button_rect = pygame.Rect(
            self.width // 2 - button_width // 2, 
            self.height - button_height - 40, 
            button_width, 
            button_height
        )
        create_button(
            self.screen, "Back", self.back_button_rect,
            bg_color=COLORS.get("BUTTON_BLUE", (40,80,120)),
            text_color=COLORS.get("TEXT_WHITE", (255,255,255)),
            font_size=FONT_SIZES["MENU_OPTION"]
        )
        game.settings_buttons['back'] = self.back_button_rect
        
        # Store current values in game object for EventHandler to use if not already there
        # The EventHandler will directly modify game.audio_settings for sliders
        game.temporary_settings = {
            'resolution_idx': self.current_resolution_idx,
            'fullscreen': self.fullscreen_enabled
        }


    def _render_slider(self, game, setting_key, label_text, y_pos, label_font, value_font):
        # Ensure game.audio_settings exists and has the key
        if not hasattr(game, 'audio_settings'):
            game.audio_settings = {}
            
        if setting_key not in game.audio_settings:
            # Initialize with default from config if not present
            game.audio_settings[setting_key] = get_setting("AUDIO", setting_key, 0.5)
            
        # Label
        label_surface = label_font.render(label_text + ":", True, COLORS["TEXT_WHITE"])
        self.screen.blit(label_surface, (self.left_margin, y_pos))

        # Slider Rail
        slider_rect = pygame.Rect(self.right_margin_controls, y_pos + label_surface.get_height() // 2 - self.slider_height // 2, self.slider_width, self.slider_height)
        pygame.draw.rect(self.screen, (100, 100, 100), slider_rect) # Rail color
        pygame.draw.rect(self.screen, (150, 150, 150), slider_rect, 2) # Border
        
        # Get the current value directly from game.audio_settings
        current_value = game.audio_settings[setting_key]
        
        # Filled part of slider to indicate value
        fill_width = int(slider_rect.width * current_value)
        fill_rect = pygame.Rect(slider_rect.x, slider_rect.y, fill_width, slider_rect.height)
        pygame.draw.rect(self.screen, COLORS.get("SLIDER_FILL", (60, 120, 200)), fill_rect)

        # Slider Handle
        handle_x = slider_rect.x + fill_width
        handle_rect = pygame.Rect(handle_x - 5, slider_rect.centery - 15, 10, 30)
        pygame.draw.rect(self.screen, COLORS.get("SETTING_VALUE", (200, 255, 200)), handle_rect) # Handle color
        pygame.draw.rect(self.screen, COLORS["TEXT_WHITE"], handle_rect, 2) # Handle border

        # Percentage Text
        percent_str = f"{int(current_value * 100)}%"
        percent_surface = value_font.render(percent_str, True, COLORS["TEXT_WHITE"])
        self.screen.blit(percent_surface, (slider_rect.right + 15, y_pos))

        # Store/update slider info for EventHandler
        game.settings_sliders[setting_key] = {
            "rect": slider_rect,
            "min": 0.0,
            "max": 1.0,
            "step": 0.01, # Standard step for volume
            "label": label_text 
        }

    def apply_settings(self):
        """Apply and save the current settings from game object and internal state"""
        # We'll need to capture game reference during render and store it
        # to access it here, since we can't use screen.game
        audio_settings = {}
        game = getattr(self, '_game_ref', None)
        
        if game and hasattr(game, 'audio_settings'):
            audio_settings = {
                "master_volume": game.audio_settings.get('master_volume', get_setting("AUDIO", "master_volume", 1.0)),
                "sfx_volume": game.audio_settings.get('sfx_volume', get_setting("AUDIO", "sfx_volume", 1.0)),
                "music_volume": game.audio_settings.get('music_volume', get_setting("AUDIO", "music_volume", 0.7)),
                "music_enabled": get_setting("AUDIO", "music_enabled", True),
                "sfx_enabled": get_setting("AUDIO", "sfx_enabled", True)
            }
            
            # Save each audio setting
            for key, value in audio_settings.items():
                update_setting("AUDIO", key, value)
        
        settings_to_save = {
            "WINDOW": {
                "width": self.resolutions[self.current_resolution_idx][0],
                "height": self.resolutions[self.current_resolution_idx][1],
                "fullscreen": self.fullscreen_enabled
            },
            "AUDIO": audio_settings
        }
        
        # Apply window settings
        window_settings = settings_to_save.get("WINDOW", {})
        update_setting("WINDOW", "width", window_settings.get("width"))
        update_setting("WINDOW", "height", window_settings.get("height"))
        update_setting("WINDOW", "fullscreen", window_settings.get("fullscreen"))
        
        return settings_to_save

    # The old handle_mouse_click, handle_mouse_release, update_slider_value methods are removed
    # Event handling is now done by EventHandler.py

    def update_local_settings_from_game(self, game_temp_settings):
        """Called by EventHandler to update renderer's local state for non-slider items"""
        if 'resolution_idx' in game_temp_settings:
            self.current_resolution_idx = game_temp_settings['resolution_idx']
        if 'fullscreen' in game_temp_settings:
            self.fullscreen_enabled = game_temp_settings['fullscreen']

    def get_current_display_settings(self):
        """Returns current display settings for EventHandler to pass to game for screen update"""
        return {
            "resolution": self.resolutions[self.current_resolution_idx],
            "fullscreen": self.fullscreen_enabled
        }