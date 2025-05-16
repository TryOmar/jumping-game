import pygame
from src.constants import WHITE, BLACK

class GameplayRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
    
    def render_game(self, game):
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
    
    def render_pause_menu(self, game):
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