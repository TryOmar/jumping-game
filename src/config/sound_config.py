"""
Sound Configuration Module for Jumping Ball Game.
This module centralizes all sound effect mappings and provides utilities for loading sounds.
"""

import os
import pygame

# Import resource_path from utility module
from src.utils.path_utils import resource_path

# Initialize pygame mixer if it hasn't been already
if not pygame.mixer.get_init():
    pygame.mixer.init()

# Base path for sound assets relative to the project root
SOUND_BASE_PATH = os.path.join("assets", "audio", "sounds")

# Volume settings - can be adjusted globally or per sound category
VOLUME_SETTINGS = {
    "MASTER": 1.0,    # Master volume multiplier (0.0 - 1.0)
    "UI": 0.7,        # User interface sounds volume
    "GAMEPLAY": 0.8,  # Gameplay sounds volume
    "MUSIC": 0.5      # Background music volume
}

# Sound effect mappings
# Maps logical sound names to relative file paths
# Format: "LOGICAL_NAME": {"file": "filename.mp3", "category": "CATEGORY", "volume": 1.0}
SOUND_EFFECTS = {
    # Button/UI sounds
    "BUTTON_CLICK": {"file": "button-click.mp3", "category": "UI", "volume": 1.0},
    "BUTTON_HOVER": {"file": "button-hover.mp3", "category": "UI", "volume": 0.5},
    
    # Game state sounds
    "GAME_START": {"file": "new-game.mp3", "category": "GAMEPLAY", "volume": 1.0},
    "LEVEL_COMPLETE": {"file": "level-complete.mp3", "category": "GAMEPLAY", "volume": 1.0},
    "RESTART_LEVEL": {"file": "restart-level.mp3", "category": "GAMEPLAY", "volume": 0.9},
    "NEXT_LEVEL": {"file": "next-level.mp3", "category": "GAMEPLAY", "volume": 1.0},
    
    # Gameplay sounds - repurposing existing files for jumping game events
    "PLAYER_JUMP": {"file": "move-empty-square.mp3", "category": "GAMEPLAY", "volume": 1.0},
    "PLAYER_LAND": {"file": "capture-sound.mp3", "category": "GAMEPLAY", "volume": 0.8},
    "PLAYER_DIE": {"file": "wrong-piece.mp3", "category": "GAMEPLAY", "volume": 1.0},
    "PLATFORM_MOVE": {"file": "obstacle-move.mp3", "category": "GAMEPLAY", "volume": 0.7},
    
    # Background music
    "BACKGROUND_MUSIC": {"file": "background-track.mp3", "category": "MUSIC", "volume": 1.0}
}

# Dictionary to store loaded Sound objects for reuse
_loaded_sounds = {}

def get_sound_path(sound_name):
    """Get the full path to a sound file given its logical name."""
    if sound_name not in SOUND_EFFECTS:
        print(f"Warning: Sound '{sound_name}' not found in sound configuration.")
        return None
    
    sound_file = SOUND_EFFECTS[sound_name]["file"]
    return os.path.join(SOUND_BASE_PATH, sound_file)

def load_sound(sound_name):
    """Load a sound by its logical name, returning a pygame.mixer.Sound object."""
    if sound_name in _loaded_sounds:
        return _loaded_sounds[sound_name]
    
    sound_path = get_sound_path(sound_name)
    if not sound_path:
        return None
    
    try:
        sound_path = os.path.join(SOUND_BASE_PATH, SOUND_EFFECTS[sound_name]["file"])
        sound = pygame.mixer.Sound(resource_path(sound_path))
        
        # Set the sound's volume based on its category and individual setting
        sound_config = SOUND_EFFECTS[sound_name]
        category_volume = VOLUME_SETTINGS.get(sound_config["category"], 1.0)
        sound_volume = sound_config.get("volume", 1.0)
        master_volume = VOLUME_SETTINGS["MASTER"]
        
        # Calculate final volume
        final_volume = sound_volume * category_volume * master_volume
        sound.set_volume(final_volume)
        
        # Cache the sound for future use
        _loaded_sounds[sound_name] = sound
        return sound
    except pygame.error as e:
        print(f"Error loading sound '{sound_name}' from {sound_path}: {e}")
        return None

def play_sound(sound_name, loops=0, max_time=0, fade_ms=0):
    """
    Play a sound by its logical name.
    
    Args:
        sound_name: The logical name of the sound to play
        loops: Number of times to repeat (-1 = infinite loop)
        max_time: Maximum play time in milliseconds
        fade_ms: Fade-in time in milliseconds
    
    Returns:
        The Channel object the sound is playing on, or None if it failed
    """
    sound = load_sound(sound_name)
    if not sound:
        return None
    
    return sound.play(loops, max_time, fade_ms)

def stop_sound(sound_name):
    """Stop a currently playing sound."""
    sound = _loaded_sounds.get(sound_name)
    if sound:
        sound.stop()

def update_volume_settings(master=None, ui=None, gameplay=None, music=None):
    """Update volume settings and apply to already loaded sounds."""
    if master is not None:
        VOLUME_SETTINGS["MASTER"] = max(0.0, min(1.0, master))
    if ui is not None:
        VOLUME_SETTINGS["UI"] = max(0.0, min(1.0, ui))
    if gameplay is not None:
        VOLUME_SETTINGS["GAMEPLAY"] = max(0.0, min(1.0, gameplay))
    if music is not None:
        VOLUME_SETTINGS["MUSIC"] = max(0.0, min(1.0, music))
    
    # Update volumes of already loaded sounds
    for sound_name, sound in _loaded_sounds.items():
        sound_config = SOUND_EFFECTS[sound_name]
        category_volume = VOLUME_SETTINGS.get(sound_config["category"], 1.0)
        sound_volume = sound_config.get("volume", 1.0)
        master_volume = VOLUME_SETTINGS["MASTER"]
        final_volume = sound_volume * category_volume * master_volume
        sound.set_volume(final_volume)

def preload_sounds(category=None):
    """
    Preload sounds to avoid loading delays during gameplay.
    Optionally filter by category (UI, GAMEPLAY, MUSIC).
    """
    for sound_name, sound_info in SOUND_EFFECTS.items():
        if category is None or sound_info["category"] == category:
            load_sound(sound_name)
    
    print(f"Preloaded {len(_loaded_sounds)} sound effects.")

def cleanup():
    """Release all loaded sounds to free memory."""
    global _loaded_sounds
    _loaded_sounds.clear() 