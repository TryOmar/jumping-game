import pygame
from src.platform import DangerousPlatform, DisappearingPlatform
from src.game_state import GameState

class CollisionHandler:
    def __init__(self, game):
        self.game = game
    
    def check_platform_collisions(self):
        """Check for collisions between player and platforms"""
        if not self.game.player or not self.game.current_map:
            return

        # Reset all platform collision flags
        for platform in self.game.current_map.platforms:
            # Don't reset platform.colliding here, let platforms manage their own state
            pass

        # Get platforms the player might be colliding with
        colliding_platforms = []
        for platform in self.game.current_map.platforms:
            # Only check for collision if we're falling onto a platform
            # Small modification: allow collision if player is at peak of jump (vel_y near zero)
            # or falling (vel_y positive), but not when rising quickly
            if self.game.player.vel_y < -2:  # Only avoid collision when player is rising quickly
                continue
                
            # Ensure the player's feet are at or below the top of the platform
            # This makes the collision detection more forgiving
            foot_y = self.game.player.y + self.game.player.radius
            if foot_y < platform.y - 2:  # Small tolerance
                continue
            
            # Complete collision check - AABB with circle
            if (self.game.player.y + self.game.player.radius > platform.y and 
                self.game.player.y - self.game.player.radius < platform.y + platform.height and
                self.game.player.x + self.game.player.radius > platform.x and 
                self.game.player.x - self.game.player.radius < platform.x + platform.width):
                
                # Check if the player is falling onto the platform (not rising through it)
                # Increased tolerance for better bouncing
                if foot_y >= platform.y and foot_y <= platform.y + 15:  # 15 pixels of tolerance
                    colliding_platforms.append(platform)
                    platform.colliding = True  # Set collision flag for visualization
        
        # Handle collision with the highest platform if there are multiple
        if colliding_platforms:
            # Find the highest platform (lowest y value)
            highest_platform = min(colliding_platforms, key=lambda p: p.y)
            
            # Debug info
            if self.game.debug_mode:
                print(f"Collision with platform {highest_platform.id} at world Y: {highest_platform.y}")
            
            # Place player on top of platform and set on_ground
            self.game.player.land(highest_platform.y)
            
            # Handle platform special effects
            self.handle_platform_effect(highest_platform)
    
    def handle_platform_effect(self, platform):
        """Handle special effects for different platform types"""
        # Call the platform's collision handler
        platform.on_collision(self.game.player)
        
        # Make the player bounce
        # Always bounce if platform is bounce_ready or if player is falling
        # onto a platform (vel_y > 0)
        # This ensures consistent bouncing regardless of auto-jump settings
        if self.game.player.vel_y > 0 or platform.bounce_ready:
            self.game.player.bounce()
            # Play jump sound when player bounces
            self.game.sound_manager.play_game_sound("jump")
        else:
            # Play landing sound when player stops on a platform
            self.game.sound_manager.play_game_sound("land")
        
        # Handle platform type specific effects
        if isinstance(platform, DangerousPlatform):
            # Play die sound
            self.game.sound_manager.play_game_sound("die")
            # Game over on dangerous platform
            self.game.state_manager.change_state(GameState.GAME_OVER, 
                                        score=abs(int(self.game.camera_y)), 
                                        reason="Danger")
        elif isinstance(platform, DisappearingPlatform):
            # Check if platform should be removed
            if platform.should_remove():
                self.game.current_map.platforms.remove(platform) 