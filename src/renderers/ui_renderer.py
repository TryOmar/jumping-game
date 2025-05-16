import pygame
from src.constants import WHITE, BLACK, GREEN, BLUE, YELLOW, RED

class UIRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
    
    def render_game_over(self, game):
        """Render game over screen"""
        # Game over text
        font = pygame.font.SysFont(None, 64)
        text = font.render("GAME OVER", True, BLACK)
        self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - 100))
        
        # Score
        score = game.state_manager.get_state_data("score")
        font = pygame.font.SysFont(None, 48)
        text = font.render(f"Score: {score}", True, BLACK)
        self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2))
        
        # Instructions
        font_small = pygame.font.SysFont(None, 24)
        text1 = font_small.render("Press 1 to return to main menu", True, BLACK)
        text2 = font_small.render("Press 2 to play again", True, BLACK)
        self.screen.blit(text1, (self.width//2 - text1.get_width()//2, self.height//2 + 80))
        self.screen.blit(text2, (self.width//2 - text2.get_width()//2, self.height//2 + 110))
    
    def render_settings(self, game):
        """Render settings screen"""
        # Will be implemented later
        pass
    
    def render_how_to_play(self, game):
        """Render instructions screen with professional layout and visual aids"""
        # Background color - soft blue gradient effect
        self.screen.fill((230, 240, 255))
        
        # Create a gradient effect (simple version)
        gradient = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for y in range(0, self.height, 2):
            alpha = 10 - int(10 * y / self.height)
            pygame.draw.line(gradient, (70, 130, 180, alpha), (0, y), (self.width, y), 2)
        self.screen.blit(gradient, (0, 0))
        
        # Header with decorative elements
        header_bg = pygame.Rect(0, 30, self.width, 60)
        pygame.draw.rect(self.screen, (70, 130, 180, 80), header_bg)
        pygame.draw.line(self.screen, (70, 130, 180), (20, 95), (self.width - 20, 95), 2)

        # Title
        title_font = pygame.font.SysFont(None, 56)
        title = title_font.render("HOW TO PLAY", True, (30, 60, 90))
        title_shadow = title_font.render("HOW TO PLAY", True, (120, 160, 200))
        self.screen.blit(title_shadow, (self.width // 2 - title.get_width() // 2 + 2, 44))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 42))

        # Main content area
        content_x = 80
        content_y = 120
        section_spacing = 30
        line_height = 30
        
        # Section font
        section_font = pygame.font.SysFont(None, 36)
        instruction_font = pygame.font.SysFont(None, 28)
        
        # 1. CONTROLS SECTION
        controls_title = section_font.render("Controls", True, (30, 60, 90))
        self.screen.blit(controls_title, (content_x, content_y))
        pygame.draw.line(self.screen, (100, 150, 200), 
                         (content_x, content_y + 35), 
                         (content_x + 200, content_y + 35), 2)
        
        controls = [
            "< > Arrow Keys: Move left and right",
            "^ Arrow Key: Manual jump (when auto-jump is off)",
            "J Key: Toggle auto-jump ON/OFF",
            "ESC Key: Pause game / Return to previous screen"
        ]
        
        control_y = content_y + 45
        for control in controls:
            text = instruction_font.render(control, True, BLACK)
            self.screen.blit(text, (content_x + 20, control_y))
            control_y += line_height
        
        # 2. PLATFORMS SECTION
        platforms_y = control_y + section_spacing
        platforms_title = section_font.render("Platforms", True, (30, 60, 90))
        self.screen.blit(platforms_title, (content_x, platforms_y))
        pygame.draw.line(self.screen, (100, 150, 200), 
                         (content_x, platforms_y + 35), 
                         (content_x + 200, platforms_y + 35), 2)
        
        # Platform types with visual examples
        platform_types = [
            ("Regular Platform", GREEN, "Stable platform to jump on"),
            ("Moving Platform", BLUE, "Moves horizontally across the screen"),
            ("Disappearing Platform", YELLOW, "Disappears after jumping on it"),
            ("Dangerous Platform", RED, "Causes game over - avoid these!")
        ]
        
        platform_y = platforms_y + 45
        for platform_name, color, description in platform_types:
            # Draw example platform
            platform_rect = pygame.Rect(content_x + 20, platform_y, 80, 20)
            pygame.draw.rect(self.screen, color, platform_rect)
            pygame.draw.rect(self.screen, BLACK, platform_rect, 2)
            
            # Draw platform name and description
            name_text = instruction_font.render(platform_name, True, BLACK)
            self.screen.blit(name_text, (content_x + 120, platform_y - 5))
            
            desc_font = pygame.font.SysFont(None, 24)
            desc_text = desc_font.render(description, True, (60, 60, 60))
            self.screen.blit(desc_text, (content_x + 120, platform_y + 15))
            
            platform_y += 50
        
        # 3. OBJECTIVES SECTION
        objectives_y = platform_y + section_spacing
        objectives_title = section_font.render("Objectives", True, (30, 60, 90))
        self.screen.blit(objectives_title, (content_x, objectives_y))
        pygame.draw.line(self.screen, (100, 150, 200), 
                         (content_x, objectives_y + 35), 
                         (content_x + 200, objectives_y + 35), 2)
        
        objectives = [
            "• Climb as high as possible by bouncing on platforms",
            "• Avoid falling off the bottom of the screen",
            "• Avoid red dangerous platforms",
            "• Reach the top of the map to complete the level"
        ]
        
        objective_y = objectives_y + 45
        for objective in objectives:
            text = instruction_font.render(objective, True, BLACK)
            self.screen.blit(text, (content_x + 20, objective_y))
            objective_y += line_height
        
        # Footer with return instruction
        footer_bg = pygame.Rect(0, self.height - 50, self.width, 50)
        pygame.draw.rect(self.screen, (70, 130, 180, 80), footer_bg)
        
        back_text = instruction_font.render("Press ESC to return to main menu", True, (30, 60, 90))
        self.screen.blit(back_text, (self.width // 2 - back_text.get_width() // 2, self.height - 35))
        
        # Page indicator (if we want to add more pages later)
        page_text = pygame.font.SysFont(None, 20).render("Page 1/1", True, (100, 100, 100))
        self.screen.blit(page_text, (self.width - 60, self.height - 30)) 