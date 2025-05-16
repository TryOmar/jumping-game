"""Default configuration values for the game."""

# Window settings
WINDOW = {
    "width": 800,
    "height": 600,
    "fps": 60,
    "title": "Jumping Ball Game"
}

# Colors
COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    
    # Additional colors
    "orange": (255, 200, 0),
    "light_blue": (0, 200, 200),
    "dark_blue": (40, 80, 120),
    "menu_bg": (50, 100, 150),
    "map_select_bg": (70, 120, 170)
}

# Player settings
PLAYER = {
    "radius": 15,
    "color": COLORS["black"],
    "gravity": 0.5,
    "jump_strength": -15,
    "move_speed": 5,
    "auto_jump_cooldown": 10,
    "auto_jump_enabled_default": True,
    "bounce_strength_multiplier": 2.0
}

# Platform settings
PLATFORM = {
    "count": 10,  # Initial platform count
    "width": 100,
    "height": 20,
    "vertical_gap": 70,
    "colors": {
        "regular": COLORS["green"],
        "moving": COLORS["blue"],
        "disappearing": COLORS["orange"],
        "dangerous": COLORS["red"]
    },
    "generation": {
        "weights": {
            "regular": 0.65,
            "moving": 0.2,
            "disappearing": 0.1,
            "dangerous": 0.05
        }
    },
    "moving": {
        "speed_min": 1.0,
        "speed_max": 3.0
    },
    "disappearing": {
        "default_jumps": 1
    }
}

# Map settings
MAP = {
    "target_height": -5000,  # Negative because we're going up
    "theme_color": (0, 150, 0),
    "platform_speed": 2,
    "platform_count_per_generation": 10
}

# Debug settings
DEBUG = {
    "enabled_default": False,
    "collision_highlight_color": COLORS["red"],
    "border_color": COLORS["black"]
}

# Audio settings (placeholders for future implementation)
AUDIO = {
    "enabled": True,
    "master_volume": 1.0,
    "sfx_volume": 1.0,
    "music_volume": 0.7
}

# UI settings
UI = {
    "auto_jump_message_duration": 2000,  # milliseconds
    "font": {
        "default": None,  # None means system default
        "title_size": 72,
        "option_size": 36,
        "small_size": 24,
        "tiny_size": 18
    },
    "menu": {
        "option_height": 40,
        "options": ["Play", "How to Play", "Settings", "Exit"]
    }
} 