import pygame
from src.constants import WHITE, BLACK
from src.config.settings import get_setting, update_setting

class SettingsRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Available resolutions
        self.resolutions = [
            (800, 600),
            (1024, 768),
            (1280, 720),
            (1366, 768),
            (1920, 1080)
        ]
        
        # Current resolution index
        self.current_resolution_idx = 0
        for i, res in enumerate(self.resolutions):
            if res == (self.width, self.height):
                self.current_resolution_idx = i
                break
        
        # Settings options (with their state)
        self.options = {
            "sound_volume": get_setting("AUDIO", "sfx_volume", 1.0),
            "music_volume": get_setting("AUDIO", "music_volume", 0.7),
            "fullscreen": pygame.display.get_surface().get_flags() & pygame.FULLSCREEN != 0
        }
        
        # Track which slider is active
        self.active_slider = None
        
        # Calculate positions for sliders
        self.slider_width = 200
        self.slider_height = 20
        
        # Position settings
        self.left_margin = 80
        self.right_margin = self.width - 300
        
        self.sound_slider_rect = pygame.Rect(
            self.right_margin, 
            200, 
            self.slider_width, 
            self.slider_height
        )
        self.music_slider_rect = pygame.Rect(
            self.right_margin, 
            250, 
            self.slider_width, 
            self.slider_height
        )
    
    def render(self, game):
        """Render the settings screen"""
        # Draw background
        background_color = (60, 80, 140)  # Dark blue background
        self.screen.fill(background_color)
        
        # Draw header
        header_font = pygame.font.SysFont(None, 64)
        header_text = header_font.render("SETTINGS", True, WHITE)
        self.screen.blit(header_text, (self.width//2 - header_text.get_width()//2, 80))
        
        # Draw setting options
        option_font = pygame.font.SysFont(None, 32)
        y_offset = 160
        
        # Resolution setting
        res_text = option_font.render("Resolution:", True, WHITE)
        self.screen.blit(res_text, (self.left_margin, y_offset))
        
        current_res = self.resolutions[self.current_resolution_idx]
        res_value = f"{current_res[0]}x{current_res[1]}"
        res_value_text = option_font.render(res_value, True, (200, 255, 200))
        self.screen.blit(res_value_text, (self.right_margin, y_offset))
        
        # Draw arrows for resolution selection
        pygame.draw.polygon(self.screen, WHITE, [
            (self.right_margin - 20, y_offset + 16),
            (self.right_margin - 10, y_offset + 8),
            (self.right_margin - 20, y_offset)
        ])
        pygame.draw.polygon(self.screen, WHITE, [
            (self.right_margin + res_value_text.get_width() + 10, y_offset + 16),
            (self.right_margin + res_value_text.get_width() + 20, y_offset + 8),
            (self.right_margin + res_value_text.get_width() + 10, y_offset)
        ])
        
        y_offset += 40
        
        # Fullscreen toggle
        fullscreen_text = option_font.render("Fullscreen:", True, WHITE)
        self.screen.blit(fullscreen_text, (self.left_margin, y_offset))
        
        fullscreen_value = "ON" if self.options["fullscreen"] else "OFF"
        fullscreen_color = (200, 255, 200) if self.options["fullscreen"] else (255, 200, 200)
        fullscreen_value_text = option_font.render(fullscreen_value, True, fullscreen_color)
        self.screen.blit(fullscreen_value_text, (self.right_margin, y_offset))
        
        y_offset += 40
        
        # Sound volume
        sound_text = option_font.render("Sound Volume:", True, WHITE)
        self.screen.blit(sound_text, (self.left_margin, y_offset))
        
        # Draw sound slider
        self.sound_slider_rect.y = y_offset
        pygame.draw.rect(self.screen, (100, 100, 100), self.sound_slider_rect)
        pygame.draw.rect(self.screen, (150, 150, 150), self.sound_slider_rect, 2)
        
        # Draw slider handle
        handle_pos = self.sound_slider_rect.x + int(self.sound_slider_rect.width * self.options["sound_volume"])
        handle_rect = pygame.Rect(handle_pos - 5, y_offset - 5, 10, 30)
        pygame.draw.rect(self.screen, (200, 255, 200), handle_rect)
        pygame.draw.rect(self.screen, WHITE, handle_rect, 2)
        
        volume_percent = f"{int(self.options['sound_volume'] * 100)}%"
        volume_text = pygame.font.SysFont(None, 24).render(volume_percent, True, WHITE)
        self.screen.blit(volume_text, (self.sound_slider_rect.right + 10, y_offset))
        
        y_offset += 40
        
        # Music volume
        music_text = option_font.render("Music Volume:", True, WHITE)
        self.screen.blit(music_text, (self.left_margin, y_offset))
        
        # Draw music slider
        self.music_slider_rect.y = y_offset
        pygame.draw.rect(self.screen, (100, 100, 100), self.music_slider_rect)
        pygame.draw.rect(self.screen, (150, 150, 150), self.music_slider_rect, 2)
        
        # Draw slider handle
        handle_pos = self.music_slider_rect.x + int(self.music_slider_rect.width * self.options["music_volume"])
        handle_rect = pygame.Rect(handle_pos - 5, y_offset - 5, 10, 30)
        pygame.draw.rect(self.screen, (200, 255, 200), handle_rect)
        pygame.draw.rect(self.screen, WHITE, handle_rect, 2)
        
        volume_percent = f"{int(self.options['music_volume'] * 100)}%"
        volume_text = pygame.font.SysFont(None, 24).render(volume_percent, True, WHITE)
        self.screen.blit(volume_text, (self.music_slider_rect.right + 10, y_offset))
        
        y_offset += 80
        
        # Controls section
        controls_text = option_font.render("Controls:", True, WHITE)
        self.screen.blit(controls_text, (self.left_margin, y_offset))
        
        control_spacing = 40
        control_y = y_offset + 40
        
        controls = [
            {"action": "Move Left", "key": "LEFT ARROW"},
            {"action": "Move Right", "key": "RIGHT ARROW"},
            {"action": "Jump", "key": "UP ARROW"},
            {"action": "Auto-Jump Toggle", "key": "J"}
        ]
        
        control_font = pygame.font.SysFont(None, 24)
        
        for i, control in enumerate(controls):
            y_pos = control_y + i * control_spacing
            
            # Draw action name
            action_text = control_font.render(control["action"] + ":", True, WHITE)
            self.screen.blit(action_text, (self.left_margin, y_pos))
            
            # Draw key binding
            key_text = control_font.render(control["key"], True, (200, 255, 200))
            self.screen.blit(key_text, (self.right_margin, y_pos))
        
        # Instructions
        instruction_font = pygame.font.SysFont(None, 24)
        instruction_text = instruction_font.render("Press ESC to return and save changes", True, WHITE)
        self.screen.blit(instruction_text, (self.width//2 - instruction_text.get_width()//2, self.height - 50))
        
    def handle_mouse_click(self, pos):
        """Handle mouse click on settings UI elements"""
        x, y = pos
        
        # Resolution arrow clicks
        res_arrow_y = 160
        current_res = self.resolutions[self.current_resolution_idx]
        res_value = f"{current_res[0]}x{current_res[1]}"
        res_text_width = pygame.font.SysFont(None, 32).render(res_value, True, (200, 255, 200)).get_width()
        
        # Left arrow
        if (self.right_margin - 20 <= x <= self.right_margin - 10) and (res_arrow_y <= y <= res_arrow_y + 16):
            self.current_resolution_idx = max(0, self.current_resolution_idx - 1)
            return True
        # Right arrow
        elif (self.right_margin + res_text_width + 10 <= x <= self.right_margin + res_text_width + 20) and (res_arrow_y <= y <= res_arrow_y + 16):
            self.current_resolution_idx = min(len(self.resolutions) - 1, self.current_resolution_idx + 1)
            return True
        
        # Check if clicked on fullscreen toggle
        fullscreen_y = 200
        fullscreen_text = pygame.font.SysFont(None, 32).render("ON" if self.options["fullscreen"] else "OFF", True, WHITE)
        if (self.right_margin <= x <= self.right_margin + fullscreen_text.get_width()) and (fullscreen_y <= y <= fullscreen_y + 30):
            self.options["fullscreen"] = not self.options["fullscreen"]
            return True
        
        # Check if clicked on sound volume slider
        if self.sound_slider_rect.collidepoint(pos):
            self.active_slider = "sound_volume"
            # Update slider position immediately
            self.update_slider_value(pos)
            return True
            
        # Check if clicked on music volume slider
        if self.music_slider_rect.collidepoint(pos):
            self.active_slider = "music_volume"
            # Update slider position immediately
            self.update_slider_value(pos)
            return True
            
        return False
    
    def handle_mouse_release(self):
        """Handle mouse button release"""
        self.active_slider = None
    
    def update_slider_value(self, pos):
        """Update slider value based on mouse position"""
        if not self.active_slider:
            return
            
        x, y = pos
        
        if self.active_slider == "sound_volume":
            # Calculate position percentage
            pos_pct = (x - self.sound_slider_rect.x) / self.sound_slider_rect.width
            # Clamp value between 0 and 1
            self.options["sound_volume"] = max(0, min(1, pos_pct))
            
        elif self.active_slider == "music_volume":
            # Calculate position percentage
            pos_pct = (x - self.music_slider_rect.x) / self.music_slider_rect.width
            # Clamp value between 0 and 1
            self.options["music_volume"] = max(0, min(1, pos_pct))
    
    def apply_settings(self):
        """Apply the current settings"""
        # Get the selected resolution
        selected_res = self.resolutions[self.current_resolution_idx]
        
        # Update internal settings
        update_setting("WINDOW", "width", selected_res[0])
        update_setting("WINDOW", "height", selected_res[1])
        update_setting("AUDIO", "sfx_volume", self.options["sound_volume"])
        update_setting("AUDIO", "music_volume", self.options["music_volume"])
        
        # Return settings that need to be applied immediately
        return {
            "resolution": selected_res,
            "fullscreen": self.options["fullscreen"]
        } 