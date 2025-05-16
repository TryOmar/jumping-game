import pygame
from src.game_state import GameState
from src.config.settings import update_setting

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
                    current_fullscreen = self.game.screen.get_flags() & pygame.FULLSCREEN
                    new_fullscreen_setting = not bool(current_fullscreen)
                    update_setting('WINDOW', 'fullscreen', new_fullscreen_setting)
                    flags = pygame.FULLSCREEN if new_fullscreen_setting else 0
                    self.game.screen = pygame.display.set_mode((self.game.width, self.game.height), flags)
                    self.game.renderer.init_renderers()
                    # This event is consumed, no further processing for F11.
                    # However, it doesn't prevent other events in the same frame from being processed by states.

                # General Escape Key Logic (can be overridden by states)
                # Note: Specific states like PLAYING/PAUSED handle ESCAPE directly in their event handlers.
                # This general ESCAPE is for menus/info screens.
                # The `handle_..._event` methods for specific states will get the ESCAPE first.
                # If they don't consume it (e.g. by returning or changing state), then this can be a fallback.
                # However, the current structure has explicit ESC handling in most relevant states.

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
            elif event.key == pygame.K_DOWN:
                self.game.selected_option = (self.game.selected_option + 1) % len(self.game.menu_options)
            elif event.key == pygame.K_RETURN:
                self._handle_menu_selection()
            elif event.key == pygame.K_ESCAPE: # Main menu specific ESC
                self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hasattr(self.game, 'menu_option_rects'):
                for i, rect in enumerate(self.game.menu_option_rects):
                    if rect.collidepoint(event.pos):
                        self.game.selected_option = i
                        self._handle_menu_selection()
                        break

    def _handle_settings_event(self, event): # Changed from _handle_settings_events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Apply settings on ESC from settings screen
                if hasattr(self.game.renderer, 'settings_renderer') and hasattr(self.game.renderer.settings_renderer, 'apply_settings'):
                     settings = self.game.renderer.settings_renderer.apply_settings()
                     self._apply_display_settings(settings) # Apply display settings if any
                self.game.apply_audio_settings() # Ensure audio settings are applied
                self.game.state_manager.change_state(GameState.MAIN_MENU) # Or return_to_previous if that's desired
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hasattr(self.game, 'settings_sliders'):
                for key, slider_info in self.game.settings_sliders.items():
                    if slider_info["rect"].collidepoint(event.pos):
                        self.dragging_slider = key
                        self._update_slider_value(key, event.pos[0], self.game.settings_sliders, self.game.audio_settings)
                        break
            if hasattr(self.game, 'settings_buttons'):
                if "back" in self.game.settings_buttons and self.game.settings_buttons["back"].collidepoint(event.pos):
                    if hasattr(self.game.renderer, 'settings_renderer') and hasattr(self.game.renderer.settings_renderer, 'apply_settings'):
                        settings = self.game.renderer.settings_renderer.apply_settings()
                        self._apply_display_settings(settings)
                    self.game.apply_audio_settings()
                    self.game.state_manager.change_state(GameState.MAIN_MENU)

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_slider and hasattr(self.game, 'settings_sliders'):
                self._update_slider_value(self.dragging_slider, event.pos[0], self.game.settings_sliders, self.game.audio_settings)
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging_slider:
                # Apply settings when slider is released (audio is live, display on exit)
                # self.game.apply_audio_settings() # Audio is applied live by _update_slider_value
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
                    self.game.init_game(custom_settings=map_config)
                    self.game.state_manager.change_state(GameState.PLAYING)

    def handle_custom_maps_event(self, event): # Changed from handle_custom_maps_events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if "play" in self.game.custom_map_buttons and self.game.custom_map_buttons["play"].collidepoint(mouse_pos):
                # Store the custom map config for retry
                self.game.state_manager.set_state_data("last_map_settings", self.game.custom_map_settings.copy())
                self.game.init_game(custom_settings=self.game.custom_map_settings)
                self.game.state_manager.change_state(GameState.PLAYING)
                return

            if "reset" in self.game.custom_map_buttons and self.game.custom_map_buttons["reset"].collidepoint(mouse_pos):
                self.game.custom_map_settings = {
                    "gravity": 0.5, "player_speed": 5, "jump_strength": 10,
                    "platform_density": 2.0, "moving_platform_pct": 25,
                    "disappearing_platform_pct": 15, "dangerous_platform_pct": 10,
                    "active_setting": None
                }
                return

            if hasattr(self.game, 'custom_map_sliders'):
                for key, slider_info in self.game.custom_map_sliders.items():
                    if slider_info["rect"].collidepoint(mouse_pos):
                        self.dragging_slider = key
                        self._update_slider_value(key, mouse_pos[0], self.game.custom_map_sliders, self.game.custom_map_settings)
                        break
        
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
                    print(f"Auto-jump {status}")
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
            if hasattr(self.game, 'game_over_button_rects'):
                    for i, rect in enumerate(self.game.game_over_button_rects):
                        if rect.collidepoint(event.pos):
                            if hasattr(self.game, 'game_over_buttons') and i < len(self.game.game_over_buttons):
                                self.game.game_over_selected_option = i
                                self._handle_game_over_selection()
                                break
                            
    def _handle_game_over_selection(self):
        if hasattr(self.game, 'game_over_buttons') and self.game.game_over_buttons and \
           0 <= self.game.game_over_selected_option < len(self.game.game_over_buttons):
            selected_action = self.game.game_over_buttons[self.game.game_over_selected_option]["action"]
            if selected_action == "retry":
                last_settings = self.game.state_manager.get_state_data().get("last_map_settings")
                if last_settings:
                    self.game.init_game(custom_settings=last_settings)
                    self.game.state_manager.change_state(GameState.PLAYING)
                else: 
                    # Fallback: if no specific last map settings, go to map select to choose one
                    self.game.state_manager.change_state(GameState.MAP_SELECT)
            elif selected_action == "main_menu":
                self.game.state_manager.change_state(GameState.MAIN_MENU)

    def _handle_how_to_play_event(self, event): # Changed from _handle_how_to_play_events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state_manager.change_state(GameState.MAIN_MENU)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            self.game.state_manager.change_state(GameState.MAIN_MENU)

    def _apply_display_settings(self, settings):
        if not settings: return
        resolution = settings.get('resolution')
        fullscreen = settings.get('fullscreen')
        current_w, current_h = self.game.screen.get_size()
        current_fullscreen = (pygame.display.get_surface().get_flags() & pygame.FULLSCREEN) != 0

        resolution_changed = resolution and (resolution[0] != current_w or resolution[1] != current_h)
        fullscreen_changed = fullscreen is not None and fullscreen != current_fullscreen

        if resolution_changed or fullscreen_changed:
            new_res = resolution if resolution_changed else (current_w, current_h)
            new_fs_flag = pygame.FULLSCREEN if (fullscreen if fullscreen_changed else current_fullscreen) else 0
            
            self.game.screen = pygame.display.set_mode(new_res, new_fs_flag)
            self.game.width, self.game.height = new_res
            self.game.renderer.screen = self.game.screen
            self.game.renderer.init_renderers()


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

        if isinstance(settings_dict.get(slider_key), int) and step == 1: # Treat as int if original and step are int
            settings_dict[slider_key] = int(value)
        else: # Otherwise, treat as float (or percentage if applicable)
            settings_dict[slider_key] = value


        if slider_key in ['master_volume', 'sfx_volume', 'music_volume']: # Apply audio immediately
             self.game.apply_audio_settings()
    
    def _handle_menu_selection(self):
        if self.game.selected_option == 0:
            self.game.state_manager.change_state(GameState.MAP_SELECT)
        elif self.game.selected_option == 1:
            self.game.state_manager.change_state(GameState.HOW_TO_PLAY)
        elif self.game.selected_option == 2:
            self.game.state_manager.change_state(GameState.SETTINGS)
        elif self.game.selected_option == 3:
            self.game.running = False