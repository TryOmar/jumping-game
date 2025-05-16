import pygame
from src.constants import WHITE, BLACK

class SettingsRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
    
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
        
        # Sound
        sound_text = option_font.render("Sound: ON", True, WHITE)
        self.screen.blit(sound_text, (self.width//2 - 150, 200))
        
        # Music
        music_text = option_font.render("Music: ON", True, WHITE)
        self.screen.blit(music_text, (self.width//2 - 150, 250))
        
        # Controls section
        controls_text = option_font.render("Controls:", True, WHITE)
        self.screen.blit(controls_text, (self.width//2 - 150, 320))
        
        control_spacing = 40
        control_y = 360
        
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
            self.screen.blit(action_text, (self.width//2 - 150, y_pos))
            
            # Draw key binding
            key_text = control_font.render(control["key"], True, (200, 255, 200))
            self.screen.blit(key_text, (self.width//2 + 80, y_pos))
        
        # Instructions
        instruction_font = pygame.font.SysFont(None, 24)
        instruction_text = instruction_font.render("Press ESC to return", True, WHITE)
        self.screen.blit(instruction_text, (self.width//2 - instruction_text.get_width()//2, self.height - 50))
        
        # Note: Future update
        note_font = pygame.font.SysFont(None, 20)
        note_text = note_font.render("Settings changes will be implemented in a future update", True, (200, 200, 200))
        self.screen.blit(note_text, (self.width//2 - note_text.get_width()//2, self.height - 80)) 