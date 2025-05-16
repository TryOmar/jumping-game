import pygame
from src.constants import WHITE, BLACK

class HowToPlayRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
    
    def render(self, game):
        """Render the how to play screen"""
        # Draw background
        background_color = (40, 90, 130)  # Blue background
        self.screen.fill(background_color)
        
        # Draw header
        header_font = pygame.font.SysFont(None, 64)
        header_text = header_font.render("HOW TO PLAY", True, WHITE)
        self.screen.blit(header_text, (self.width//2 - header_text.get_width()//2, 60))
        
        # Draw game instructions
        instruction_spacing = 40
        start_y = 150
        
        instructions = [
            {"title": "Goal", "text": "Climb as high as possible by jumping on platforms."},
            {"title": "Controls", "text": "LEFT/RIGHT: Move side to side"},
            {"title": "", "text": "UP: Jump higher when on a platform"},
            {"title": "", "text": "J: Toggle auto-jump (jumps automatically on platform contact)"},
            {"title": "Platforms", "text": "Green: Regular platforms"},
            {"title": "", "text": "Blue: Moving platforms"},
            {"title": "", "text": "Yellow: Disappearing platforms (disappear after jumping)"},
            {"title": "", "text": "Red: Dangerous platforms (game over on contact)"},
            {"title": "Tips", "text": "- You can wrap around screen edges"},
            {"title": "", "text": "- Aim for higher platforms to climb faster"},
            {"title": "", "text": "- Watch your timing on moving platforms"}
        ]
        
        title_font = pygame.font.SysFont(None, 30)
        text_font = pygame.font.SysFont(None, 24)
        
        for i, instr in enumerate(instructions):
            y_pos = start_y + i * instruction_spacing
            
            # Draw the title if it's not empty
            if instr["title"]:
                title_text = title_font.render(instr["title"] + ":", True, (255, 255, 150))
                self.screen.blit(title_text, (self.width//2 - 200, y_pos))
            
            # Draw the instruction text
            instr_text = text_font.render(instr["text"], True, WHITE)
            x_pos = self.width//2 - 70 if instr["title"] else self.width//2 - 50
            self.screen.blit(instr_text, (x_pos, y_pos))
        
        # Draw some visual examples
        example_size = 20
        example_x = self.width//2 - 250
        
        # Draw platform examples
        pygame.draw.rect(self.screen, (0, 255, 0), (example_x, start_y + 4*instruction_spacing, example_size*3, example_size//2))
        pygame.draw.rect(self.screen, (0, 0, 255), (example_x, start_y + 5*instruction_spacing, example_size*3, example_size//2))
        pygame.draw.rect(self.screen, (255, 255, 0), (example_x, start_y + 6*instruction_spacing, example_size*3, example_size//2))
        pygame.draw.rect(self.screen, (255, 0, 0), (example_x, start_y + 7*instruction_spacing, example_size*3, example_size//2))
        
        # Draw player example
        pygame.draw.circle(self.screen, BLACK, (example_x + example_size//2, start_y + instruction_spacing), example_size//2)
        
        # Instructions to return
        footer_font = pygame.font.SysFont(None, 24)
        footer_text = footer_font.render("Press ESC to return to main menu", True, WHITE)
        self.screen.blit(footer_text, (self.width//2 - footer_text.get_width()//2, self.height - 40)) 