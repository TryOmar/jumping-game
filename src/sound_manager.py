"""
Sound Manager for Jumping Ball Game.
This module provides a simple interface for playing sounds and managing audio settings.
"""

import pygame
from src.config import sound_config
from src.config.settings import get_setting

class SoundManager:
    """Handles playing sounds, music, and managing audio settings."""
    
    def __init__(self, game):
        """Initialize the sound manager."""
        self.game = game
        self.enabled = True
        self.music_enabled = True
        self.sfx_enabled = True
        
        # Ensure pygame mixer is initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        # Preload common UI sounds to avoid delays
        sound_config.preload_sounds("UI")
        
        # Track currently playing music
        self.current_music = None
    
    def play_sound(self, sound_name):
        """Play a sound effect if sound effects are enabled."""
        if not self.enabled or not self.sfx_enabled:
            return None
        
        # Refresh volume settings from config before playing
        self._refresh_volume_settings()
            
        return sound_config.play_sound(sound_name)
    
    def play_music(self, music_name, loops=-1):
        """Play background music if music is enabled."""
        if not self.enabled or not self.music_enabled:
            return
        
        # Refresh volume settings from config before playing
        self._refresh_volume_settings()
            
        # Stop any currently playing music
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            
        music_path = sound_config.get_sound_path(music_name)
        if not music_path:
            return
            
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(sound_config.VOLUME_SETTINGS["MUSIC"] * 
                                          sound_config.VOLUME_SETTINGS["MASTER"])
            pygame.mixer.music.play(loops)
            self.current_music = music_name
        except pygame.error as e:
            print(f"Error playing music '{music_name}': {e}")
    
    def stop_music(self):
        """Stop the currently playing music."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.current_music = None
    
    def pause_music(self):
        """Pause the currently playing music."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Unpause the music if it was paused."""
        pygame.mixer.music.unpause()
    
    def toggle_sounds(self):
        """Toggle sound effects on/off."""
        self.sfx_enabled = not self.sfx_enabled
        return self.sfx_enabled
    
    def toggle_music(self):
        """Toggle music on/off."""
        self.music_enabled = not self.music_enabled
        
        if self.music_enabled and self.current_music:
            # Resume playing music
            self.play_music(self.current_music)
        elif not self.music_enabled:
            # Stop music
            self.stop_music()
            
        return self.music_enabled
    
    def toggle_all_audio(self):
        """Toggle all audio (both music and sound effects)."""
        self.enabled = not self.enabled
        
        if not self.enabled:
            # Stop all audio
            self.stop_music()
            # Could also stop all playing sound effects if needed
            
        elif self.enabled and self.music_enabled and self.current_music:
            # Resume music if it was playing
            self.play_music(self.current_music)
            
        return self.enabled
    
    def update_volume(self, master=None, sfx=None, music=None):
        """Update volume settings."""
        # Print debug info to verify volume values
        print(f"Updating volumes - Master: {master}, SFX: {sfx}, Music: {music}")
        
        # Update the volume settings in sound_config
        sound_config.update_volume_settings(
            master=master,
            ui=sfx,  # UI category is used for sound effects
            gameplay=sfx,  # Gameplay sounds also use the sfx volume
            music=music
        )
        
        # Update music volume if it's currently playing
        if pygame.mixer.music.get_busy():
            music_vol = sound_config.VOLUME_SETTINGS["MUSIC"] * sound_config.VOLUME_SETTINGS["MASTER"]
            print(f"Setting music volume to: {music_vol}")
            pygame.mixer.music.set_volume(music_vol)
    
    def play_ui_sound(self, action="click"):
        """Play UI sounds based on action type."""
        if action == "click":
            self.play_sound("BUTTON_CLICK")
        elif action == "hover":
            self.play_sound("BUTTON_HOVER")
    
    def play_game_sound(self, action):
        """Play gameplay sounds based on action type."""
        sound_mapping = {
            "jump": "PLAYER_JUMP",
            "land": "PLAYER_LAND",
            "die": "PLAYER_DIE",
            "platform_move": "PLATFORM_MOVE",
            "level_complete": "LEVEL_COMPLETE",
            "game_start": "GAME_START",
            "restart": "RESTART_LEVEL"
        }
        
        if action in sound_mapping:
            self.play_sound(sound_mapping[action])
    
    def cleanup(self):
        """Clean up resources when shutting down."""
        self.stop_music()
        sound_config.cleanup()
    
    def _refresh_volume_settings(self):
        """Get the latest volume settings from configuration."""
        # Get current settings
        master_volume = get_setting('AUDIO', 'master_volume', 1.0)
        sfx_volume = get_setting('AUDIO', 'sfx_volume', 1.0)
        music_volume = get_setting('AUDIO', 'music_volume', 0.7)
        
        # Apply them to sound config
        sound_config.update_volume_settings(
            master=master_volume,
            ui=sfx_volume,
            gameplay=sfx_volume,
            music=music_volume
        ) 