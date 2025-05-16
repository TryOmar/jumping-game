import pygame
from src.game_state import GameState

class EventHandler:
    def __init__(self, game):
        self.game = game
        self.dragging_slider = None  # Track which slider is being dragged
    
    def handle_events(self):
        """Process all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
                
            # Process keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Escape behaves differently based on state
                    if self.game.state_manager.is_state(GameState.PLAYING):
                        self.game.state_manager.change_state(GameState.PAUSED)
                    elif self.game.state_manager.is_state(GameState.PAUSED):
                        self.game.state_manager.change_state(GameState.PLAYING)
                    elif self.game.state_manager.is_state(GameState.MAIN_MENU):
                        self.game.running = False
                    elif self.game.state_manager.is_state(GameState.MAP_SELECT):
                        # Return to main menu when on map selection screen
                        self.game.state_manager.change_state(GameState.MAIN_MENU)
                    elif self.game.state_manager.is_state(GameState.OFFICIAL_MAPS):
                        # Return to map selection screen
                        self.game.state_manager.change_state(GameState.MAP_SELECT)
                    elif self.game.state_manager.is_state(GameState.CUSTOM_MAPS):
                        # Return to map selection screen
                        self.game.state_manager.change_state(GameState.MAP_SELECT)
                    else:
                        self.game.state_manager.return_to_previous()
                
                # Toggle debug mode with F1
                if event.key == pygame.K_F1:
                    self.game.toggle_debug()
                
                # Toggle auto-jump with J key
                if event.key == pygame.K_j and self.game.player:
                    enabled = self.game.player.toggle_auto_jump()
                    status = "enabled" if enabled else "disabled"
                    print(f"Auto-jump {status}")
                    
                    # Add visual feedback when auto-jump is toggled
                    self.game.show_auto_jump_message = True
                    self.game.auto_jump_message_time = pygame.time.get_ticks()
                    self.game.auto_jump_status = enabled
                
                # Main menu controls
                if self.game.state_manager.is_state(GameState.MAIN_MENU):
                    if event.key == pygame.K_UP:
                        self.game.selected_option = max(0, self.game.selected_option - 1)
                    elif event.key == pygame.K_DOWN:
                        self.game.selected_option = min(len(self.game.menu_options) - 1, self.game.selected_option + 1)
                    elif event.key == pygame.K_RETURN:
                        self._handle_menu_selection()
                
                # Game over screen controls
                elif self.game.state_manager.is_state(GameState.GAME_OVER):
                    if event.key == pygame.K_UP:
                        self.game.game_over_selected_option = max(0, self.game.game_over_selected_option - 1)
                    elif event.key == pygame.K_DOWN:
                        self.game.game_over_selected_option = min(1, self.game.game_over_selected_option + 1)
                    elif event.key == pygame.K_RETURN:
                        self._handle_game_over_selection()
                
                # Temporary state change keys for testing
                if event.key == pygame.K_1:
                    self.game.state_manager.change_state(GameState.MAIN_MENU)
                elif event.key == pygame.K_2:
                    # Always reinitialize the game when starting a new game
                    self.game.state_manager.change_state(GameState.PLAYING)
                    self.game.init_game()
                elif event.key == pygame.K_3:
                    self.game.state_manager.change_state(GameState.GAME_OVER, score=100)
            
            # Handle mouse events for menu
            if self.game.state_manager.is_state(GameState.MAIN_MENU):
                if event.type == pygame.MOUSEMOTION:
                    # Check if mouse is over any menu option
                    mouse_pos = pygame.mouse.get_pos()
                    for i, option in enumerate(self.game.menu_options):
                        option_rect = self._get_menu_option_rect(i)
                        if option_rect.collidepoint(mouse_pos):
                            self.game.selected_option = i
                            break
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    # Check if clicking on a menu option
                    mouse_pos = pygame.mouse.get_pos()
                    for i, option in enumerate(self.game.menu_options):
                        option_rect = self._get_menu_option_rect(i)
                        if option_rect.collidepoint(mouse_pos):
                            self.game.selected_option = i
                            self._handle_menu_selection()
                            break
            
            # Handle mouse events for map selection screen
            elif self.game.state_manager.is_state(GameState.MAP_SELECT):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check if the user clicked on the Official Maps button
                    if hasattr(self.game, 'map_selection_buttons'):
                        if self.game.map_selection_buttons["official"].collidepoint(mouse_pos):
                            print("Official Maps selected")
                            # Navigate to the official maps screen
                            self.game.state_manager.change_state(GameState.OFFICIAL_MAPS)
                            
                        elif self.game.map_selection_buttons["custom"].collidepoint(mouse_pos):
                            print("Custom Maps selected")
                            # Navigate to the custom maps screen
                            self.game.state_manager.change_state(GameState.CUSTOM_MAPS)
            
            # Handle mouse events for official maps screen
            elif self.game.state_manager.is_state(GameState.OFFICIAL_MAPS):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check if a map was clicked
                    if hasattr(self.game, 'official_map_buttons'):
                        for map_key, map_rect in self.game.official_map_buttons.items():
                            if map_rect.collidepoint(mouse_pos):
                                if map_key == "map1":
                                    print("Map 1 selected")
                                    # Start the game with Map 1
                                    self.game.state_manager.change_state(GameState.PLAYING)
                                    self.game.init_game()
                                # Additional maps would be handled here
            
            # Handle mouse events for custom maps screen
            elif self.game.state_manager.is_state(GameState.CUSTOM_MAPS):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check if clicking on a slider
                    if hasattr(self.game, 'custom_map_sliders'):
                        for key, slider_info in self.game.custom_map_sliders.items():
                            if slider_info["rect"].collidepoint(mouse_pos):
                                self.dragging_slider = key
                                # Immediately adjust the value based on click position
                                self._update_slider_value(key, mouse_pos[0])
                                break
                    
                    # Check if clicking on a button
                    if hasattr(self.game, 'custom_map_buttons'):
                        if "play" in self.game.custom_map_buttons and self.game.custom_map_buttons["play"].collidepoint(mouse_pos):
                            print("Starting custom map with settings:", self.game.custom_map_settings)
                            # Pass custom settings to game state
                            self.game.state_manager.change_state(GameState.PLAYING, custom_settings=self.game.custom_map_settings)
                            self.game.init_game(custom_settings=self.game.custom_map_settings)
                        
                        elif "reset" in self.game.custom_map_buttons and self.game.custom_map_buttons["reset"].collidepoint(mouse_pos):
                            # Reset settings to default
                            self.game.custom_map_settings = {
                                "gravity": 0.5,
                                "player_speed": 5,
                                "jump_strength": 10,
                                "platform_density": 2.0,
                                "moving_platform_pct": 25,
                                "disappearing_platform_pct": 15,
                                "dangerous_platform_pct": 10,
                                "active_setting": None
                            }
                
                # Handle dragging sliders
                if event.type == pygame.MOUSEMOTION and self.dragging_slider:
                    self._update_slider_value(self.dragging_slider, event.pos[0])
                
                # Handle releasing slider
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.dragging_slider = None
            
            # Handle mouse events for game over screen
            elif self.game.state_manager.is_state(GameState.GAME_OVER):
                if event.type == pygame.MOUSEMOTION:
                    # Check if mouse is over any option
                    mouse_pos = pygame.mouse.get_pos()
                    if hasattr(self.game, 'game_over_buttons'):
                        for i, button_rect in enumerate(self.game.game_over_buttons):
                            if button_rect.collidepoint(mouse_pos):
                                self.game.game_over_selected_option = i
                                break
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    # Check if clicking on an option
                    mouse_pos = pygame.mouse.get_pos()
                    if hasattr(self.game, 'game_over_buttons'):
                        for i, button_rect in enumerate(self.game.game_over_buttons):
                            if button_rect.collidepoint(mouse_pos):
                                self.game.game_over_selected_option = i
                                self._handle_game_over_selection()
                                break
    
    def _update_slider_value(self, slider_key, mouse_x):
        """Update slider value based on mouse position"""
        if not hasattr(self.game, 'custom_map_sliders'):
            return
            
        slider_info = self.game.custom_map_sliders[slider_key]
        slider_rect = slider_info["rect"]
        
        # Calculate normalized position (0-1)
        slider_width = slider_rect.width
        slider_start = slider_rect.left
        slider_rel_pos = max(0, min(mouse_x - slider_start, slider_width))
        normalized_pos = slider_rel_pos / slider_width
        
        # Calculate actual value based on range
        min_val = slider_info["min"]
        max_val = slider_info["max"]
        step = slider_info["step"]
        
        # Calculate value and round to nearest step
        raw_value = min_val + normalized_pos * (max_val - min_val)
        steps = round((raw_value - min_val) / step)
        value = min_val + steps * step
        
        # Ensure value is within bounds
        value = max(min_val, min(max_val, value))
        
        # Update the setting
        self.game.custom_map_settings[slider_key] = value
    
    def _handle_menu_selection(self):
        """Handle menu option selection"""
        if self.game.selected_option == 0:  # Play
            # Changed to show map selection instead of directly starting the game
            self.game.state_manager.change_state(GameState.MAP_SELECT)
        elif self.game.selected_option == 1:  # How to Play
            self.game.state_manager.change_state(GameState.HOW_TO_PLAY)
        elif self.game.selected_option == 2:  # Settings
            self.game.state_manager.change_state(GameState.SETTINGS)
        elif self.game.selected_option == 3:  # Exit
            self.game.running = False
    
    def _get_menu_option_rect(self, index):
        """Get the rectangle for a menu option for collision detection"""
        option_height = 40
        start_y = self.game.height // 2
        option_y = start_y + index * option_height
        
        # Approximate width based on text length
        option_width = len(self.game.menu_options[index]) * 20
        option_x = self.game.width // 2 - option_width // 2
        
        return pygame.Rect(option_x, option_y, option_width, option_height)

    # Add this new method to handle game over option selection
    def _handle_game_over_selection(self):
        """Handle game over option selection"""
        if self.game.game_over_selected_option == 0:  # Try Again
            print("Try Again selected")
            # Restart the game with same map
            self.game.state_manager.change_state(GameState.PLAYING)
            self.game.init_game()
        elif self.game.game_over_selected_option == 1:  # Main Menu
            print("Return to Main Menu selected")
            self.game.state_manager.change_state(GameState.MAIN_MENU) 