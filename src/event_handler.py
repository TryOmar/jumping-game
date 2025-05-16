import pygame
from src.game_state import GameState
from src.config.settings import update_setting, get_setting

class EventHandler:
    def __init__(self, game):
        self.game = game
        self.dragging_slider = None # For settings screen
    
    def handle_events(self):
        """Process all game events"""
        for event in pygame.event.get(): # Iterate through each event
            if event.type == pygame.QUIT:
                self.game.running = False
                return # Exit early if QUIT

            # --- Global Key Presses (Processed for all states if not consumed by state-specific handler) ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    # This specific F11 handling directly toggles based on current display state
                    # and updates settings. It might be better to consolidate with settings screen logic.
                    current_fullscreen_flags = pygame.display.get_surface().get_flags() & pygame.FULLSCREEN
                    new_fullscreen_setting = not bool(current_fullscreen_flags)
                    update_setting('WINDOW', 'fullscreen', new_fullscreen_setting)
                    self.game.renderer.settings_renderer.fullscreen_enabled = new_fullscreen_setting # Update renderer state
                    if hasattr(self.game, 'temporary_settings'):
                        self.game.temporary_settings['fullscreen'] = new_fullscreen_setting

                    display_settings = self.game.renderer.settings_renderer.get_current_display_settings()
                    self._apply_display_settings(display_settings) # Apply immediately

                if event.key == pygame.K_F1:
                    self.game.toggle_debug()
                
                # Auto-jump toggle is specific to PLAYING state, handled there.

                # Temporary state change keys (should ideally be removed or guarded for debug builds)
                # if event.key == pygame.K_1:
                #     self.game.state_manager.change_state(GameState.MAIN_MENU)
                # elif event.key == pygame.K_2:
                #     self.game.state_manager.change_state(GameState.PLAYING)
                #     self.game.init_game()
                # elif event.key == pygame.K_3:
                #     self.game.state_manager.change_state(GameState.GAME_OVER, score=100)


            # --- State-specific event handling: Pass single event ---
            current_state = self.game.state_manager.current_state

            if current_state == GameState.MAIN_MENU:
                self._handle_main_menu_event(event)
            elif current_state == GameState.SETTINGS:
                self._handle_settings_event(event)
            elif current_state == GameState.MAP_SELECT:
                self.handle_map_selection_event(event)
            elif current_state == GameState.OFFICIAL_MAPS:
                self.handle_official_maps_event(event)
            elif current_state == GameState.CUSTOM_MAPS:
                self.handle_custom_maps_event(event)
            elif current_state == GameState.PLAYING:
                self._handle_playing_event(event)
            elif current_state == GameState.PAUSED:
                self._handle_pause_menu_event(event)
            elif current_state == GameState.GAME_OVER:
                self._handle_game_over_event(event)
            elif current_state == GameState.HOW_TO_PLAY:
                self._handle_how_to_play_event(event)

    def _handle_main_menu_event(self, event): # Changed from _handle_main_menu_events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.game.selected_option = (self.game.selected_option - 1) % len(self.game.menu_options)
                self.game.sound_manager.play_ui_sound("hover")
            elif event.key == pygame.K_DOWN:
                self.game.selected_option = (self.game.selected_option + 1) % len(self.game.menu_options)
                self.game.sound_manager.play_ui_sound("hover")
            elif event.key == pygame.K_RETURN:
                self.game.sound_manager.play_ui_sound("click")
                self._handle_menu_selection()
            elif event.key == pygame.K_ESCAPE: # Main menu specific ESC
                self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hasattr(self.game, 'menu_option_rects'):
                for i, rect in enumerate(self.game.menu_option_rects):
                    if rect.collidepoint(event.pos):
                        self.game.selected_option = i
                        self.game.sound_manager.play_ui_sound("click")
                        self._handle_menu_selection()
                        break

    def _handle_settings_event(self, event):
        settings_renderer = self.game.renderer.settings_renderer
        # Initialize temporary_settings from renderer if not already on game object
        if not hasattr(self.game, 'temporary_settings') or self.game.temporary_settings is None:
            if hasattr(settings_renderer, 'current_resolution_idx') and hasattr(settings_renderer, 'fullscreen_enabled'):
                 self.game.temporary_settings = {
                    'resolution_idx': settings_renderer.current_resolution_idx,
                    'fullscreen': settings_renderer.fullscreen_enabled
                }
            else: # Fallback if renderer not fully initialized with these attributes
                self.game.temporary_settings = {
                    'resolution_idx': 0, # Default
                    'fullscreen': get_setting("WINDOW", "fullscreen", False)
                }

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                applied_settings = settings_renderer.apply_settings()
                self._apply_display_settings(applied_settings.get("WINDOW"))
                self.game.apply_audio_settings()
                self.game.state_manager.change_state(GameState.MAIN_MENU)
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            # Slider interaction
            if hasattr(self.game, 'settings_sliders'):
                for key, slider_info in self.game.settings_sliders.items():
                    if slider_info["rect"].collidepoint(mouse_pos):
                        self.dragging_slider = key
                        self._update_slider_value(key, mouse_pos[0], self.game.settings_sliders, self.game.audio_settings)
                        # No break here, allow other buttons to be checked if somehow overlapping (though unlikely)
            
            # Button interaction
            if hasattr(self.game, 'settings_buttons'):
                buttons = self.game.settings_buttons
                for button_key, rect in buttons.items():
                    if rect.collidepoint(mouse_pos):
                        if button_key == "back":
                            applied_settings = settings_renderer.apply_settings()
                            self._apply_display_settings(applied_settings.get("WINDOW"))
                            self.game.apply_audio_settings()
                            self.game.state_manager.change_state(GameState.MAIN_MENU)
                            return # Event handled
                        elif button_key == 'res_left':
                            if 'resolution_idx' in self.game.temporary_settings:
                                current_idx = self.game.temporary_settings['resolution_idx']
                                num_res = len(settings_renderer.resolutions)
                                self.game.temporary_settings['resolution_idx'] = (current_idx - 1 + num_res) % num_res
                                settings_renderer.update_local_settings_from_game(self.game.temporary_settings)
                                
                                # Apply display settings immediately
                                display_settings = settings_renderer.get_current_display_settings()
                                self._apply_display_settings(display_settings)
                                
                                # Play sound effect for button click
                                self.game.sound_manager.play_ui_sound("click")
                            return # Event handled
                        elif button_key == 'res_right':
                            if 'resolution_idx' in self.game.temporary_settings:
                                current_idx = self.game.temporary_settings['resolution_idx']
                                num_res = len(settings_renderer.resolutions)
                                self.game.temporary_settings['resolution_idx'] = (current_idx + 1) % num_res
                                settings_renderer.update_local_settings_from_game(self.game.temporary_settings)
                                
                                # Apply display settings immediately
                                display_settings = settings_renderer.get_current_display_settings()
                                self._apply_display_settings(display_settings)
                                
                                # Play sound effect for button click
                                self.game.sound_manager.play_ui_sound("click")
                            return # Event handled
                        elif button_key == 'fullscreen_toggle':
                            if 'fullscreen' in self.game.temporary_settings:
                                self.game.temporary_settings['fullscreen'] = not self.game.temporary_settings['fullscreen']
                                settings_renderer.update_local_settings_from_game(self.game.temporary_settings)
                                
                                # Apply display settings immediately
                                display_settings = settings_renderer.get_current_display_settings()
                                self._apply_display_settings(display_settings)
                                
                                # Play sound effect for button click
                                self.game.sound_manager.play_ui_sound("click")
                            return # Event handled

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_slider and hasattr(self.game, 'settings_sliders'):
                self._update_slider_value(self.dragging_slider, event.pos[0], self.game.settings_sliders, self.game.audio_settings)
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging_slider:
                self.dragging_slider = None

    def handle_map_selection_event(self, event): # Changed from handle_map_selection_events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hasattr(self.game, 'map_selection_buttons'):
                for button_name, button_rect in self.game.map_selection_buttons.items():
                    if button_rect.collidepoint(event.pos):
                        if button_name == "official":
                            self.game.state_manager.change_state(GameState.OFFICIAL_MAPS)
                        elif button_name == "custom":
                            self.game.state_manager.change_state(GameState.CUSTOM_MAPS)
                        return # Event handled
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state_manager.change_state(GameState.MAIN_MENU)

    def handle_official_maps_event(self, event): # Changed from handle_official_maps_events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if "play" in self.game.official_map_buttons and self.game.official_map_buttons["play"].collidepoint(mouse_pos):
                selected_map_key = self.game.selected_official_map
                if selected_map_key in self.game.official_map_configs:
                    map_config = self.game.official_map_configs[selected_map_key]
                    # Store the selected official map config for retry
                    self.game.state_manager.set_state_data("last_map_settings", map_config)
                    self.game.state_manager.set_state_data("last_map_id", selected_map_key) # Store map_id for high scores
                    self.game.init_game(custom_settings=map_config)
                    self.game.state_manager.change_state(GameState.PLAYING)
                return 

            for map_key, map_rect in self.game.official_map_buttons.items():
                if map_key != "play" and map_rect.collidepoint(mouse_pos):
                    if map_key in self.game.official_map_configs:
                        self.game.selected_official_map = map_key
                    return
                        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state_manager.change_state(GameState.MAP_SELECT)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                selected_map_key = self.game.selected_official_map
                if selected_map_key in self.game.official_map_configs:
                    map_config = self.game.official_map_configs[selected_map_key]
                    self.game.state_manager.set_state_data("last_map_settings", map_config)
                    self.game.state_manager.set_state_data("last_map_id", selected_map_key) # Store map_id
                    self.game.init_game(custom_settings=map_config)
                    self.game.state_manager.change_state(GameState.PLAYING)

    def handle_custom_maps_event(self, event): # Changed from handle_custom_maps_events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if "play" in self.game.custom_map_buttons and self.game.custom_map_buttons["play"].collidepoint(mouse_pos):
                # Store the custom map config for retry
                self.game.state_manager.set_state_data("last_map_settings", self.game.custom_map_settings.copy())
                self.game.state_manager.set_state_data("last_map_id", "custom") # Store map_id
                self.game.init_game(custom_settings=self.game.custom_map_settings)
                self.game.state_manager.change_state(GameState.PLAYING)
                return

            if "reset" in self.game.custom_map_buttons and self.game.custom_map_buttons["reset"].collidepoint(mouse_pos):
                self.game.custom_map_settings = {
                    "gravity": 0.5, "player_speed": 5, "jump_strength": 10,
                    "platform_density": 2.0, "moving_platform_pct": 25,
                    "disappearing_platform_pct": 15, "dangerous_platform_pct": 10,
                    "active_setting": None # This might need to be reset if used by renderer
                }
                # Potentially call a method on custom_maps_renderer to reset its internal state if any
                return

            if hasattr(self.game, 'custom_map_sliders'):
                for key, slider_info in self.game.custom_map_sliders.items():
                    if slider_info["rect"].collidepoint(mouse_pos):
                        self.dragging_slider = key
                        self._update_slider_value(key, mouse_pos[0], self.game.custom_map_sliders, self.game.custom_map_settings)
                        break # Assuming only one slider can be dragged at a time
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_slider and hasattr(self.game, 'custom_map_sliders'):
                self._update_slider_value(self.dragging_slider, event.pos[0], self.game.custom_map_sliders, self.game.custom_map_settings)
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging_slider:
                self.dragging_slider = None
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state_manager.change_state(GameState.MAP_SELECT)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.game.state_manager.set_state_data("last_map_settings", self.game.custom_map_settings.copy())
                self.game.state_manager.set_state_data("last_map_id", "custom") # Store map_id
                self.game.init_game(custom_settings=self.game.custom_map_settings)
                self.game.state_manager.change_state(GameState.PLAYING)

    def _handle_playing_event(self, event): # Changed from _handle_playing_events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state_manager.change_state(GameState.PAUSED)
            # elif event.key == pygame.K_p: # Debug: Toggle pause (already handled by ESC)
            #     self.game.state_manager.change_state(GameState.PAUSED)
            # elif event.key == pygame.K_d: # Debug: Toggle debug mode (handled globally by F1)
            #     self.game.toggle_debug()
            elif event.key == pygame.K_j: 
                if self.game.player: # Ensure player exists
                    enabled = self.game.player.toggle_auto_jump()
                    status = "enabled" if enabled else "disabled"
                    # print(f"Auto-jump {status}") # Reduce console spam, handled by visual
                    self.game.show_auto_jump_message = True
                    self.game.auto_jump_message_time = pygame.time.get_ticks()
                    self.game.auto_jump_status = enabled
                    
    def _handle_pause_menu_event(self, event): # Changed from _handle_pause_menu_events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state_manager.change_state(GameState.PLAYING) 
            elif event.key == pygame.K_RETURN:
                if hasattr(self.game, 'pause_selected_option'):
                    if self.game.pause_selected_option == 0: 
                        self.game.state_manager.change_state(GameState.PLAYING)
                    elif self.game.pause_selected_option == 1: 
                        self.game.state_manager.change_state(GameState.MAIN_MENU)
            elif event.key == pygame.K_UP:
                if hasattr(self.game, 'pause_selected_option') and hasattr(self.game, 'pause_menu_options'):
                    self.game.pause_selected_option = (self.game.pause_selected_option - 1) % len(self.game.pause_menu_options)
            elif event.key == pygame.K_DOWN:
                    if hasattr(self.game, 'pause_selected_option') and hasattr(self.game, 'pause_menu_options'):
                        self.game.pause_selected_option = (self.game.pause_selected_option + 1) % len(self.game.pause_menu_options)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hasattr(self.game, 'pause_button_rects'):
                for option, rect in self.game.pause_button_rects.items():
                    if rect.collidepoint(event.pos):
                        if option == "Resume":
                            self.game.state_manager.change_state(GameState.PLAYING)
                        elif option == "Main Menu":
                            self.game.state_manager.change_state(GameState.MAIN_MENU)
                        break

    def _handle_game_over_event(self, event): # Changed from _handle_game_over_events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if hasattr(self.game, 'game_over_buttons') and self.game.game_over_buttons: # Check not empty
                    self.game.game_over_selected_option = (self.game.game_over_selected_option - 1) % len(self.game.game_over_buttons)
            elif event.key == pygame.K_DOWN:
                if hasattr(self.game, 'game_over_buttons') and self.game.game_over_buttons: # Check not empty
                    self.game.game_over_selected_option = (self.game.game_over_selected_option + 1) % len(self.game.game_over_buttons)
            elif event.key == pygame.K_RETURN:
                self._handle_game_over_selection()
            elif event.key == pygame.K_ESCAPE: # Allow ESC from game over to go to main menu
                 self.game.state_manager.change_state(GameState.MAIN_MENU)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hasattr(self.game, 'game_over_button_rects'): # Ensure rects are available
                for i, rect in enumerate(self.game.game_over_button_rects):
                    if rect.collidepoint(event.pos):
                        if hasattr(self.game, 'game_over_buttons') and i < len(self.game.game_over_buttons):
                            self.game.game_over_selected_option = i
                            self._handle_game_over_selection()
                            break
                            
    def _handle_game_over_selection(self):
        """Handle selection in game over menu"""
        self.game.sound_manager.play_ui_sound("click")
        selected = self.game.game_over_selected_option
        buttons = self.game.game_over_buttons
        
        if selected < len(buttons):
            action = buttons[selected]["action"]
            
            if action == "try_again":
                # Get last game settings if available
                last_settings = self.game.state_manager.get_state_data("last_map_settings")
                if last_settings:
                    self.game.init_game(custom_settings=last_settings)
                else:
                    self.game.init_game()  # Start with default settings
                self.game.state_manager.change_state(GameState.PLAYING)
                self.game.sound_manager.play_game_sound("restart")
            elif action == "main_menu":
                self.game.state_manager.change_state(GameState.MAIN_MENU)
            elif action == "exit":
                self.game.running = False

    def _handle_how_to_play_event(self, event): # Changed from _handle_how_to_play_events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state_manager.change_state(GameState.MAIN_MENU)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            # Any click on how to play screen returns to main menu
            self.game.state_manager.change_state(GameState.MAIN_MENU)

    def _apply_display_settings(self, window_settings):
        if not window_settings: return

        resolution = window_settings.get('resolution')
        fullscreen = window_settings.get('fullscreen')
        current_w, current_h = self.game.screen.get_size()
        current_fullscreen_flag = (pygame.display.get_surface().get_flags() & pygame.FULLSCREEN) != 0

        resolution_changed = False
        if resolution and (resolution[0] != current_w or resolution[1] != current_h):
            resolution_changed = True
        
        fullscreen_changed = False
        if fullscreen is not None and fullscreen != current_fullscreen_flag:
            fullscreen_changed = True

        if resolution_changed or fullscreen_changed:
            new_res = resolution if resolution_changed else (current_w, current_h)
            new_fs_flag = pygame.FULLSCREEN if (fullscreen if fullscreen_changed else current_fullscreen_flag) else 0
            
            self.game.screen = pygame.display.set_mode(new_res, new_fs_flag)
            self.game.width, self.game.height = new_res
            if hasattr(self.game, 'renderer') and self.game.renderer is not None:
                self.game.renderer.screen = self.game.screen # Update renderer's screen reference
                self.game.renderer.init_renderers() # Re-initialize all sub-renderers

    def _update_slider_value(self, slider_key, mouse_x, sliders_dict, settings_dict):
        slider_info = sliders_dict.get(slider_key)
        if not slider_info: return

        slider_rect = slider_info["rect"]
        min_val, max_val, step = slider_info["min"], slider_info["max"], slider_info["step"]
        
        relative_x = max(0, min(mouse_x - slider_rect.left, slider_rect.width))
        normalized_pos = relative_x / slider_rect.width
        raw_value = min_val + normalized_pos * (max_val - min_val)
        
        if step != 0:
            value = min_val + round((raw_value - min_val) / step) * step
        else:
            value = raw_value
        value = round(max(min_val, min(max_val, value)), 2) # Round to 2 for floats, clamp

        # Ensure the settings_dict (e.g., game.audio_settings) is correctly updated
        if isinstance(settings_dict.get(slider_key), int) and step == 1: 
            settings_dict[slider_key] = int(value)
        else: 
            settings_dict[slider_key] = value

        # Apply audio immediately if it's an audio setting
        if slider_key in ['master_volume', 'sfx_volume', 'music_volume'] and settings_dict is self.game.audio_settings:
            print(f"Slider moved: {slider_key} = {value}")
            self.game.apply_audio_settings()
            
            # Play a test sound when moving the sfx slider
            if slider_key == 'sfx_volume' and not pygame.mixer.get_busy():
                self.game.sound_manager.play_ui_sound("hover")
    
    def _handle_menu_selection(self):
        """Handle selection from main menu"""
        self.game.sound_manager.play_ui_sound("click")
        selected_option = self.game.menu_options[self.game.selected_option]
        
        if selected_option == "Play":
            self.game.state_manager.change_state(GameState.MAP_SELECT)
        elif selected_option == "How to Play":
            self.game.state_manager.change_state(GameState.HOW_TO_PLAY)
        elif selected_option == "Settings":
            # No need to call init_settings() as it doesn't exist
            self.game.state_manager.change_state(GameState.SETTINGS)
        elif selected_option == "Exit":
            self.game.running = False