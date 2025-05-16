"""
Constants module for backward compatibility.
This file provides the same constants as before but now sources them from the new configuration system.
"""

from src.config.settings import get_window_width, get_window_height, get_fps, get_color, get_player_setting, get_platform_setting

# Game constants
SCREEN_WIDTH = get_window_width()
SCREEN_HEIGHT = get_window_height()
FPS = get_fps()

# Colors
WHITE = get_color('white')
BLACK = get_color('black')
RED = get_color('red')
GREEN = get_color('green')
BLUE = get_color('blue')
YELLOW = get_color('yellow')

# Physics
GRAVITY = get_player_setting('gravity')
JUMP_STRENGTH = get_player_setting('jump_strength')
MOVE_SPEED = get_player_setting('move_speed')

# Game settings
PLATFORM_COUNT = get_platform_setting('count')

# Platform settings
PLATFORM_WIDTH = get_platform_setting('width')
PLATFORM_HEIGHT = get_platform_setting('height')
PLATFORM_COLORS = [
    get_platform_setting('colors', 'regular'),
    get_platform_setting('colors', 'moving'),
    get_platform_setting('colors', 'disappearing'),
    get_color('orange')  # Disappearing (low jumps)
] 