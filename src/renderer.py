import pygame
from src.constants import WHITE, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, GREEN, BLUE, YELLOW, RED
from src.game_state import GameState

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
    
    def render(self, game):
        """Draw everything to the screen"""
        # Clear the screen
        self.screen.fill(WHITE)
        
        # Render based on game state
        if game.state_manager.is_state(GameState.MAIN_MENU):
            self._render_main_menu(game)
        elif game.state_manager.is_state(GameState.MAP_SELECT):
            self._render_map_select(game)
        elif game.state_manager.is_state(GameState.PLAYING):
            self._render_game(game)
        elif game.state_manager.is_state(GameState.PAUSED):
            self._render_game(game)  # Render game in background
            self._render_pause_menu(game)
        elif game.state_manager.is_state(GameState.GAME_OVER):
            self._render_game_over(game)
        elif game.state_manager.is_state(GameState.SETTINGS):
            self._render_settings(game)
        elif game.state_manager.is_state(GameState.HOW_TO_PLAY):
            self._render_how_to_play(game)
        
        # Update the display
        pygame.display.flip()
    
    def _render_main_menu(self, game):
        """Render the main menu screen"""
        # Draw background
        background_color = (50, 100, 150)  # Nice blue background
        self.screen.fill(background_color)
        
        # Draw game title
        title_font = pygame.font.SysFont(None, 72)
        title_text = title_font.render("JUMPING BALL", True, WHITE)
        self.screen.blit(title_text, (self.width//2 - title_text.get_width()//2, 100))
        
        # Draw decorative circles
        pygame.draw.circle(self.screen, BLACK, (self.width//2, 200), 30)
        pygame.draw.circle(self.screen, (200, 200, 0), (self.width//2 - 80, 220), 15)
        pygame.draw.circle(self.screen, (0, 200, 200), (self.width//2 + 80, 220), 15)
        
        # Draw menu options
        option_height = 40
        start_y = self.height // 2
        
        for i, option in enumerate(game.menu_options):
            # Determine if this option is selected
            is_selected = (i == game.selected_option)
            
            # Choose font color based on selection
            color = BLACK if not is_selected else (255, 0, 0)
            
            # Create option text
            option_font = pygame.font.SysFont(None, 36)
            option_text = option_font.render(option, True, color)
            
            # Draw option text
            option_y = start_y + i * option_height
            option_x = self.width//2 - option_text.get_width()//2
            self.screen.blit(option_text, (option_x, option_y))
            
            # Draw indicator if selected
            if is_selected:
                # Draw arrow or highlight
                pygame.draw.polygon(self.screen, (255, 0, 0), [
                    (option_x - 20, option_y + option_text.get_height()//2),
                    (option_x - 10, option_y + option_text.get_height()//2 - 5),
                    (option_x - 10, option_y + option_text.get_height()//2 + 5),
                ])
        
        # Draw footer text
        footer_font = pygame.font.SysFont(None, 20)
        footer_text = footer_font.render("Use arrow keys to select, Enter to confirm", True, WHITE)
        self.screen.blit(footer_text, (self.width//2 - footer_text.get_width()//2, self.height - 50))
    
    def _render_map_select(self, game):
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
        
        # Display available maps preview (will be expanded later)
        preview_font = pygame.font.SysFont(None, 28)
        preview_text = preview_font.render("Available Maps:", True, WHITE)
        self.screen.blit(preview_text, (self.width//2 - preview_text.get_width()//2, 350))
        
        # Small map previews
        map_preview_size = 100
        preview_y = 400
        
        # Map 1 - Current working map
        map1_rect = pygame.Rect(self.width//2 - 230, preview_y, map_preview_size, map_preview_size)
        pygame.draw.rect(self.screen, GREEN, map1_rect)
        pygame.draw.rect(self.screen, WHITE, map1_rect, 2)
        map1_text = desc_font.render("Map 1", True, BLACK)
        self.screen.blit(map1_text, (map1_rect.centerx - map1_text.get_width()//2, 
                                   map1_rect.centery - map1_text.get_height()//2))
        map1_status = desc_font.render("Available", True, WHITE)
        self.screen.blit(map1_status, (map1_rect.centerx - map1_status.get_width()//2, 
                                    map1_rect.bottom + 10))
        
        # Maps 2-4 - Coming Soon
        coming_soon_maps = [
            {"name": "Map 2", "x": self.width//2 - 80, "color": BLUE},
            {"name": "Map 3", "x": self.width//2 + 70, "color": YELLOW},
            {"name": "Map 4", "x": self.width//2 + 220, "color": RED}
        ]
        
        for map_info in coming_soon_maps:
            map_rect = pygame.Rect(map_info["x"], preview_y, map_preview_size, map_preview_size)
            
            # Semi-transparent gray overlay to indicate unavailability
            pygame.draw.rect(self.screen, map_info["color"], map_rect)
            
            # Gray overlay
            overlay = pygame.Surface((map_preview_size, map_preview_size), pygame.SRCALPHA)
            overlay.fill((100, 100, 100, 150))  # Semi-transparent gray
            self.screen.blit(overlay, map_rect)
            
            pygame.draw.rect(self.screen, WHITE, map_rect, 2)
            
            # Map name
            map_text = desc_font.render(map_info["name"], True, WHITE)
            self.screen.blit(map_text, (map_rect.centerx - map_text.get_width()//2, 
                                     map_rect.centery - map_text.get_height()//2))
            
            # Coming soon text
            soon_text = desc_font.render("Coming Soon", True, (255, 200, 0))
            self.screen.blit(soon_text, (map_rect.centerx - soon_text.get_width()//2, 
                                      map_rect.bottom + 10))
        
        # Instructions
        instruction_font = pygame.font.SysFont(None, 24)
        instruction_text = instruction_font.render("Click on a map type to select, or press ESC to return", True, WHITE)
        self.screen.blit(instruction_text, (self.width//2 - instruction_text.get_width()//2, self.height - 40))
        
        # Store button rectangles in the game object for click detection
        game.map_selection_buttons = {
            "official": official_rect,
            "custom": custom_rect,
            "map1": map1_rect
        }
    
    def _render_game(self, game):
        """Render the actual gameplay"""
        if game.current_map:
            game.current_map.draw(self.screen, game.camera_y)
            if game.debug_mode:
                game.current_map.draw_platform_info(self.screen, game.camera_y)
                font = pygame.font.SysFont(None, 24)
                text = font.render(f"Camera Y (World): {game.camera_y:.0f}", True, BLACK)
                self.screen.blit(text, (10, 130))
                coord_text = font.render("World Y → Screen Y (World Y - Camera Y)", True, BLACK)
                self.screen.blit(coord_text, (10, 190))
        
        if game.player:
            game.player.draw(self.screen, game.camera_y)
            
            if game.debug_mode:
                font = pygame.font.SysFont(None, 24)
                player_screen_y_debug = game.player.y - game.camera_y
                text = font.render(f"Player (World Y): {game.player.y:.0f} (Screen Y): {player_screen_y_debug:.0f}", True, BLACK)
                self.screen.blit(text, (10, 160))
                vel_text = font.render(f"Vel: ({game.player.vel_x:.1f}, {game.player.vel_y:.1f})", True, BLACK)
                self.screen.blit(vel_text, (10, 175))
                jump_text = font.render(f"On Ground: {game.player.on_ground} | Jumping: {game.player.is_jumping} | Cool: {game.player.auto_jump_cooldown}", True, BLACK)
                self.screen.blit(jump_text, (10, 220))
                auto_jump_text = font.render(f"Auto-Jump: {'ON' if game.player.auto_jump_enabled else 'OFF'}", True, (0, 128, 0) if game.player.auto_jump_enabled else (200, 0, 0))
                self.screen.blit(auto_jump_text, (10, 240))
        
        font = pygame.font.SysFont(None, 36)
        score = game.state_manager.get_state_data("score")
        text = font.render(f"Score: {score}", True, BLACK)
        self.screen.blit(text, (10, 10))
        
        # Show auto-jump toggle instructions and status
        font_small = pygame.font.SysFont(None, 24)
        auto_status = "ON" if game.player and game.player.auto_jump_enabled else "OFF"
        status_color = (0, 128, 0) if game.player and game.player.auto_jump_enabled else (200, 0, 0)
        text = font_small.render(f"Auto-Jump: {auto_status} (Press J to toggle)", True, status_color)
        self.screen.blit(text, (10, 45))
        
        # Display auto-jump toggle message if active
        if game.show_auto_jump_message:
            # Check if message should still be displayed (show for 2 seconds)
            current_time = pygame.time.get_ticks()
            if current_time - game.auto_jump_message_time < 2000:  # 2000ms = 2s
                # Create a semi-transparent background for the message
                msg_surface = pygame.Surface((400, 80), pygame.SRCALPHA)
                msg_surface.fill((0, 0, 0, 128))  # Black with 50% transparency
                
                # Add message text
                msg_font = pygame.font.SysFont(None, 36)
                msg_status = "ENABLED" if game.auto_jump_status else "DISABLED"
                msg_color = (0, 255, 0) if game.auto_jump_status else (255, 0, 0)
                msg_text = msg_font.render(f"Auto-Jump {msg_status}", True, msg_color)
                
                # Center the message on the screen
                msg_x = self.width // 2 - msg_surface.get_width() // 2
                msg_y = self.height // 2 - msg_surface.get_height() // 2
                
                # Draw message background and text
                self.screen.blit(msg_surface, (msg_x, msg_y))
                self.screen.blit(msg_text, (msg_x + 200 - msg_text.get_width() // 2, 
                                          msg_y + 40 - msg_text.get_height() // 2))
            else:
                # Time expired, hide message
                game.show_auto_jump_message = False
        
        if game.debug_mode:
            font = pygame.font.SysFont(None, 24)
            text = font.render("DEBUG MODE (F1 to toggle)", True, (255, 0, 0))
            self.screen.blit(text, (self.width - text.get_width() - 10, 10))
    
    def _render_pause_menu(self, game):
        """Render pause menu overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% transparency
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        font = pygame.font.SysFont(None, 48)
        text = font.render("PAUSED", True, WHITE)
        self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - text.get_height()//2))
        
        # Instructions
        font_small = pygame.font.SysFont(None, 24)
        text = font_small.render("Press ESC to resume, 1 for main menu", True, WHITE)
        self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2 + 50))
    
    def _render_game_over(self, game):
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
    
    def _render_settings(self, game):
        """Render settings screen"""
        # Will be implemented later
        pass
    
    def _render_how_to_play(self, game):
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