from enum import Enum

class GameState(Enum):
    """Enum representing different game states"""
    MAIN_MENU = 0
    MAP_SELECT = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    SETTINGS = 5
    HOW_TO_PLAY = 6
    
class StateManager:
    """Manages transitions between different game states"""
    def __init__(self, initial_state=GameState.MAIN_MENU):
        self.current_state = initial_state
        self.previous_state = None
        
        # Dictionary to store state-specific data
        self.state_data = {
            GameState.MAIN_MENU: {},
            GameState.MAP_SELECT: {},
            GameState.PLAYING: {
                "score": 0,
                "current_map": None,
                "camera_y": 0
            },
            GameState.PAUSED: {},
            GameState.GAME_OVER: {
                "score": 0,
                "reason": None  # Reason for game over
            },
            GameState.SETTINGS: {
                "sound_on": True,
                "music_on": True,
                "controls": {
                    "left": "LEFT",
                    "right": "RIGHT",
                    "jump": "UP",
                    "shoot": "SPACE"
                }
            },
            GameState.HOW_TO_PLAY: {}
        }
    
    def change_state(self, new_state, **kwargs):
        """
        Change the current game state
        
        Args:
            new_state (GameState): The new state to change to
            **kwargs: Optional data to store with the new state
        """
        self.previous_state = self.current_state
        self.current_state = new_state
        
        # Update state data with provided kwargs
        if kwargs:
            for key, value in kwargs.items():
                self.state_data[new_state][key] = value
    
    def return_to_previous(self):
        """Return to the previous game state"""
        if self.previous_state:
            temp = self.current_state
            self.current_state = self.previous_state
            self.previous_state = temp
    
    def get_state_data(self, key=None):
        """Get data for the current state"""
        if key:
            return self.state_data[self.current_state].get(key)
        return self.state_data[self.current_state]
    
    def set_state_data(self, key, value):
        """Set data for the current state"""
        self.state_data[self.current_state][key] = value
    
    def is_state(self, state):
        """Check if the current state matches the given state"""
        return self.current_state == state 