import pygame
from src.ui_styles import COLORS, FONT_SIZES, DIMENSIONS, create_centered_text

class HowToPlayRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
    
        # Position settings - consistent with settings screen
        self.left_margin = 80
        self.right_margin = self.width - 350  # Increased margin to prevent text cutoff
        
        # Use smaller font sizes to fit everything on one screen
        self.title_font_size = FONT_SIZES["STANDARD_TEXT"] - 4  # Slightly smaller
        self.text_font_size = FONT_SIZES["SMALL_TEXT"] - 2      # Slightly smaller
    
    def render(self, game):
        """Render the how to play screen"""
        # Draw background
        self.screen.fill(COLORS["BG_HOW_TO_PLAY"])
        
        # Draw header with background for better separation
        header_bg = pygame.Rect(0, 20, self.width, 50)  # Reduced height
        pygame.draw.rect(self.screen, (30, 70, 110), header_bg)
        
        create_centered_text(
            self.screen,
            "HOW TO PLAY",
            FONT_SIZES["TITLE_MEDIUM"],  # Slightly smaller title
            COLORS["TEXT_WHITE"],
            25  # Moved up
        )
        
        # Draw decorative line under header
        pygame.draw.rect(
            self.screen, 
            COLORS["TEXT_WHITE"], 
            (self.width//2 - 180, 80, 360, 2)  # Moved up and thinner
        )
        
        # Common fonts - reduced size
        title_font = pygame.font.SysFont(None, self.title_font_size)
        text_font = pygame.font.SysFont(None, self.text_font_size)
        
        # Layout configuration - reduced spacing
        section_spacing = 20  # Decreased space between sections
        line_spacing = 28     # Decreased line spacing
        
        # Starting Y position after header - moved up
        current_y = 100
        
        # Function to draw section with background
        def draw_section(title, y_pos, height, items=None):
            # Add extra height to ensure text fits
            actual_height = height + 15  # Extra padding
            
            # Draw section background for better visual hierarchy
            section_bg = pygame.Rect(40, y_pos - 5, self.width - 80, actual_height)
            pygame.draw.rect(self.screen, (50, 80, 120, 128), section_bg, 0, 8)
            pygame.draw.rect(self.screen, (70, 100, 150), section_bg, 2, 8)
            
            # Draw title
            title_surf = title_font.render(title, True, (255, 240, 150))
            self.screen.blit(title_surf, (self.left_margin, y_pos))
            
            return y_pos + 30  # Return position for content (reduced from 40)
        
        # --- GOAL SECTION ---
        goal_title_y = current_y
        content_y = draw_section("Goal:", goal_title_y, 30)  # Reduced height
        
        # Draw content - centered better
        text_surf = text_font.render("Climb as high as possible by jumping on platforms.", True, (230, 230, 230))
        text_width = text_surf.get_width()
        self.screen.blit(text_surf, (self.width//2 - text_width//2, content_y - 15))  # Better centering
        
        current_y += 50  # Reduced spacing
        
        # --- CONTROLS SECTION ---
        controls_title_y = current_y
        controls_height = 5 * line_spacing
        content_y = draw_section("Controls:", controls_title_y, controls_height)
        
        # Draw content with improved alignment
        controls = [
            "Move Left",
            "Move Right",
            "Jump Higher",
            "Toggle Auto-Jump",
            "Pause / Return"
        ]
        
        control_keys = [
            "LEFT ARROW",
            "RIGHT ARROW",
            "UP ARROW",
            "J Key",
            "ESC Key"
        ]
        
        # Player icon for visual reference
        pygame.draw.circle(
            self.screen, 
            COLORS["TEXT_BLACK"],
            (self.left_margin + 10, content_y + 3),  # Adjusted position
            6  # Smaller
        )
        # Add white border
        pygame.draw.circle(
            self.screen, 
            COLORS["TEXT_WHITE"],
            (self.left_margin + 10, content_y + 3),  # Adjusted position
            6,  # Smaller
            1
        )
        
        for i, (control, key) in enumerate(zip(controls, control_keys)):
            line_y = content_y + (i * line_spacing)
            # Control action - left-aligned
            text_surf = text_font.render(control, True, (230, 230, 230))
            text_x = self.left_margin + 45  # Closer to left margin
            self.screen.blit(text_surf, (text_x, line_y - 5))  # Adjusted y position
            
            # Control key binding - extreme right-aligned with fixed position
            key_surf = text_font.render(key, True, (200, 255, 200))
            key_x = self.width - 200  # Moved more to the left to prevent overflow
            self.screen.blit(key_surf, (key_x, line_y - 5))  # Adjusted y position
        
        current_y = controls_title_y + controls_height + 25  # Less space after controls
        
        # --- PLATFORMS SECTION ---
        platforms_title_y = current_y
        platforms_height = 4 * line_spacing + 10
        content_y = draw_section("Platforms:", platforms_title_y, platforms_height)
        
        # Platform types with descriptions
        platforms = [
            {"name": "Regular Platforms", "color": COLORS["PLATFORM_REGULAR"], "description": "Safe to land on"},
            {"name": "Moving Platforms", "color": COLORS["PLATFORM_MOVING"], "description": "Move horizontally"},
            {"name": "Disappearing Platforms", "color": COLORS["PLATFORM_DISAPPEARING"], "description": "Vanish after jumping"},
            {"name": "Dangerous Platforms", "color": COLORS["PLATFORM_DANGEROUS"], "description": "Game over on contact"}
        ]
        
        platform_width = 60  # Smaller
        platform_height = 15  # Smaller
        
        # Draw platform examples with cleaner layout
        for i, platform in enumerate(platforms):
            line_y = content_y + (i * line_spacing)
            
            # Draw platform examples
            pygame.draw.rect(
                self.screen,
                platform["color"],
                (self.left_margin + 10, line_y - 2, platform_width, platform_height)  # Adjusted y position
            )
            # Add white border
            pygame.draw.rect(
                self.screen,
                COLORS["TEXT_WHITE"],
                (self.left_margin + 10, line_y - 2, platform_width, platform_height),  # Adjusted y position
                1
            )
            
            # Platform name - left side
            text_surf = text_font.render(platform["name"], True, (230, 230, 230))
            name_x = self.left_margin + 80  # Closer to left
            self.screen.blit(text_surf, (name_x, line_y - 5))  # Adjusted y position
            
            # Platform description - right-aligned with fixed position
            desc_surf = text_font.render(platform["description"], True, (200, 255, 200))
            desc_x = self.width - 200  # Moved more to the left to prevent overflow
            self.screen.blit(desc_surf, (desc_x, line_y - 5))  # Adjusted y position
        
        current_y = platforms_title_y + platforms_height + 25  # Less space after platforms
        
        # --- TIPS SECTION - Refined spacing ---
        tips_title_y = current_y
        tips_height = 70  # Fixed height for all tips
        content_y = draw_section("Tips:", tips_title_y, tips_height)
        
        # Combined tips to save space and shorter text
        tips = [
            "• Wrap around screen edges",
            "• Aim for higher platforms",
            "• Watch timing on platforms",
            "• Toggle auto-jump styles"
        ]
        
        # Draw tips in one row with two columns - better aligned
        col1_tips = tips[:2]
        col2_tips = tips[2:]
        
        # Column positions adjusted for better balance
        col1_x = self.left_margin + 45
        col2_x = self.width//2 + 30  # Adjusted for better spacing
        
        # Draw first column
        for i, tip in enumerate(col1_tips):
            line_y = content_y + (i * line_spacing)
            text_surf = text_font.render(tip, True, (230, 230, 230))
            self.screen.blit(text_surf, (col1_x, line_y - 5))  # Adjusted y position
        
        # Draw second column
        for i, tip in enumerate(col2_tips):
            line_y = content_y + (i * line_spacing)
            text_surf = text_font.render(tip, True, (230, 230, 230))
            self.screen.blit(text_surf, (col2_x, line_y - 5))  # Adjusted y position
        
        # --- FOOTER ---
        footer_bg = pygame.Rect(0, self.height - 40, self.width, 40)  # Smaller footer
        pygame.draw.rect(self.screen, (30, 70, 110), footer_bg)
        
        create_centered_text(
            self.screen,
            "Press ESC to return to main menu",
            FONT_SIZES["FOOTER_NOTE"] - 2,  # Smaller footer text
            COLORS["TEXT_WHITE"],
            self.height - 25
        )