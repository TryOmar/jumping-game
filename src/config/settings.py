"""
Game configuration system.
Provides access to all game settings and constants.
"""

from src.config.default_config import *

# This dictionary can be used to store user-defined overrides for settings
# It would be populated from a settings file or UI
user_config = {}

def get_setting(section, key, default=None):
    """
    Get a configuration value from the specified section and key.
    
    Args:
        section (str): The configuration section (e.g., 'WINDOW', 'PLAYER')
        key (str): The specific setting key
        default: Value to return if the setting doesn't exist
        
    Returns:
        The configuration value or default if not found
    """
    # First check if there's a user override
    if section in user_config and key in user_config[section]:
        return user_config[section][key]
    
    # Then check if it exists in the default config
    config_section = globals().get(section)
    if config_section and key in config_section:
        return config_section[key]
    
    # Return default if not found
    return default

def update_setting(section, key, value):
    """
    Update a configuration value in the user_config.
    
    Args:
        section (str): The configuration section (e.g., 'WINDOW', 'PLAYER')
        key (str): The specific setting key
        value: The new value for the setting
    """
    if section not in user_config:
        user_config[section] = {}
    
    user_config[section][key] = value

def save_user_config():
    """
    Save user configuration to a file (to be implemented).
    This would allow persistent settings between game sessions.
    """
    # TODO: Implement saving settings to a JSON or similar file
    pass

def load_user_config():
    """
    Load user configuration from a file (to be implemented).
    This would restore saved settings when the game starts.
    """
    # TODO: Implement loading settings from a JSON or similar file
    pass

# Convenience functions for common settings
def get_window_width():
    return get_setting('WINDOW', 'width')

def get_window_height():
    return get_setting('WINDOW', 'height')

def get_fps():
    return get_setting('WINDOW', 'fps')

def get_color(name):
    return get_setting('COLORS', name)

def get_player_setting(key):
    return get_setting('PLAYER', key)

def get_platform_setting(key, subkey=None):
    if subkey:
        return get_setting('PLATFORM', key).get(subkey)
    return get_setting('PLATFORM', key) 