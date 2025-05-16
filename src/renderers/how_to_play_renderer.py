import pygame
from src.ui_styles import COLORS, FONT_SIZES, DIMENSIONS, create_centered_text

class HowToPlayRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
    
    def render(self, game):
        """Render the how to play screen"""
        # Draw background
        self.screen.fill(COLORS["BG_HOW_TO_PLAY"])
        
        # Draw header
        create_centered_text(
            self.screen,
            "HOW TO PLAY",
            FONT_SIZES["TITLE_LARGE"],
            COLORS["TEXT_WHITE"],
            60
        )
        
        # Draw decorative line under header
        pygame.draw.rect(
            self.screen, 
            COLORS["TEXT_WHITE"], 
            (self.width//2 - 180, 120, 360, 3)
        )
        
        # Common fonts
        title_font = pygame.font.SysFont(None, FONT_SIZES["STANDARD_TEXT"])
        text_font = pygame.font.SysFont(None, FONT_SIZES["SMALL_TEXT"])
        
        # Layout configuration
        section_spacing = 45  # Space between major sections
        line_spacing = 35     # Space between lines within a section
        
        # Improved column positions for better alignment
        left_col = int(self.width * 0.15)    # Left column for section titles and platform examples
        right_col = int(self.width * 0.35)   # Right column start position for text
        max_line_width = int(self.width * 0.5)  # Maximum width for text lines
        
        # Starting Y position after header
        current_y = 170
        
        # --- GOAL SECTION ---
        goal_title_y = current_y
        # Draw title
        title_surf = title_font.render("Goal:", True, COLORS["OPTION_TEXT"])
        self.screen.blit(title_surf, (left_col, goal_title_y))
        
        # Draw content
        text_surf = text_font.render("Climb as high as possible by jumping on platforms.", True, COLORS["TEXT_WHITE"])
        self.screen.blit(text_surf, (right_col, goal_title_y))
        
        current_y += section_spacing
        
        # --- CONTROLS SECTION ---
        controls_title_y = current_y
        # Draw title
        title_surf = title_font.render("Controls:", True, COLORS["OPTION_TEXT"])
        self.screen.blit(title_surf, (left_col, controls_title_y))
        
        # Draw content - one line at a time with improved alignment
        controls = [
            "LEFT/RIGHT: Move side to side",
            "UP: Jump higher when on a platform",
            "J: Toggle auto-jump (jumps automatically on contact)",
            "ESC: Pause game / Return to previous screen"
        ]
        
        for i, line in enumerate(controls):
            line_y = controls_title_y + (i * line_spacing)
            text_surf = text_font.render(line, True, COLORS["TEXT_WHITE"])
            self.screen.blit(text_surf, (right_col, line_y))
            
            # Draw player example at control section
            if i == 0:  # Position next to the first control line
                pygame.draw.circle(
                    self.screen, 
                    COLORS["TEXT_BLACK"],
                    (left_col + 15, line_y + 8),
                    12
                )
                # Add white border
                pygame.draw.circle(
                    self.screen, 
                    COLORS["TEXT_WHITE"],
                    (left_col + 15, line_y + 8),
                    12,
                    1
                )
        
        current_y += section_spacing + (len(controls) - 1) * line_spacing
        
        # --- PLATFORMS SECTION ---
        platforms_title_y = current_y
        # Draw title
        title_surf = title_font.render("Platforms:", True, COLORS["OPTION_TEXT"])
        self.screen.blit(title_surf, (left_col, platforms_title_y))
        
        # Platform types with shorter descriptions
        platforms = [
            {"color": COLORS["PLATFORM_REGULAR"], "text": "Green: Regular platforms"},
            {"color": COLORS["PLATFORM_MOVING"], "text": "Blue: Moving platforms"},
            {"color": COLORS["PLATFORM_DISAPPEARING"], "text": "Yellow: Disappearing platforms"},
            {"color": COLORS["PLATFORM_DISAPPEARING"], "text_2": "(disappear after jumping)"},
            {"color": COLORS["PLATFORM_DANGEROUS"], "text": "Red: Dangerous platforms"},
            {"color": COLORS["PLATFORM_DANGEROUS"], "text_2": "(game over on contact)"}
        ]
        
        platform_width = 70
        platform_height = 18
        
        # Draw platform examples with cleaner layout
        actual_platforms = 0
        for i, platform in enumerate(platforms):
            line_y = platforms_title_y + (i * line_spacing)
            
            # Only draw platform examples for main entries
            if "text" in platform:
                # Draw platform examples
                pygame.draw.rect(
                    self.screen,
                    platform["color"],
                    (left_col, line_y + 4, platform_width, platform_height)
                )
                # Add white border
                pygame.draw.rect(
                    self.screen,
                    COLORS["TEXT_WHITE"],
                    (left_col, line_y + 4, platform_width, platform_height),
                    1
                )
                actual_platforms += 1
            
            # Draw platform text (either main text or continuation)
            if "text" in platform:
                text_surf = text_font.render(platform["text"], True, COLORS["TEXT_WHITE"])
                self.screen.blit(text_surf, (right_col, line_y))
            elif "text_2" in platform:
                # This is a continuation line - indent it
                text_surf = text_font.render(platform["text_2"], True, COLORS["TEXT_WHITE"])
                self.screen.blit(text_surf, (right_col + 20, line_y))
        
        current_y += section_spacing + (len(platforms) - 1) * line_spacing
        
        # --- TIPS SECTION ---
        tips_title_y = current_y
        # Draw title
        title_surf = title_font.render("Tips:", True, COLORS["OPTION_TEXT"])
        self.screen.blit(title_surf, (left_col, tips_title_y))
        
        # Tips content with cleaner formatting
        tips = [
            "You can wrap around screen edges",
            "Aim for higher platforms to climb faster",
            "Watch your timing on moving platforms"
        ]
        
        for i, tip in enumerate(tips):
            line_y = tips_title_y + (i * line_spacing)
            text_surf = text_font.render(tip, True, COLORS["TEXT_WHITE"])
            self.screen.blit(text_surf, (right_col, line_y))
        
        # --- FOOTER ---
        create_centered_text(
            self.screen,
            "Press ESC to return to main menu",
            FONT_SIZES["FOOTER_NOTE"],
            COLORS["TEXT_WHITE"],
            int(self.height * 0.9)
        )