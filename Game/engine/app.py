import pygame, json, os, sys

import engine.libs.SceneService as SceneService
import engine.libs.GuiService as GuiService
import engine.libs.TweenService as TweenService
import engine.libs.TransitionService as TransitionService
import engine.libs.DebugService as DebugService
import engine.libs.ViewportModule as ViewportModule
 

        
class App:
    """
    Main game/app loop class for the PyRed Engine.
    """

    def __init__(self, override_config = False, preview_mode = False):
        self._override_config = override_config
        self._preview_mode = preview_mode
        self._override_config_text = """{
            "app": {
                "settings": {
                    "resolution": "1280x720",
                    "v-sync": 0,
                    "max-fps": 60,
                    "window-title-name": "Citrus Cats TD",
                    "window-icon-path": "ico.png",
                    "start-scene": "user_login"
                }
            },
            "workspace": {
                "settings": {
                    "use-opengl": false,
                    "debug-mode": false, 
                    "performance-mode": false
                }
            },
            "camera": {
                "settings": {
                    "enable-zooming": false 
                }
            },
            "experimental": {
                "features": {
                    "enable-window-blurring": false,
                    "color-to-blur": [2, 127, 252],
                    "discord-rich-presence": true 
                }
            },
            "discord-rpc": {
                
            }
            }"""            
        
  
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.load_engine()
        self.load_services()
        self.load_scenes()

    def load_config(self):
        """
        Loads game settings from a "config.json" file.
        """
        self.service_registry = []
        
        if not self._override_config:
            
            
            with open("config.json", "r") as conf:
                data_raw = json.load(conf)
                
                app_settings = data_raw["app"]["settings"]
                workspace_settings = data_raw["workspace"]["settings"]
                camera_settings = data_raw["camera"]["settings"]

                return app_settings, workspace_settings, camera_settings

            if self.workspace_settings["performance-mode"]:
                pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])
        else:

            data_raw = json.loads(self._override_config_text)
                
            app_settings = data_raw["app"]["settings"]
            workspace_settings = data_raw["workspace"]["settings"]
            camera_settings = data_raw["camera"]["settings"]

            return app_settings, workspace_settings, camera_settings

    def load_engine(self):
        """
        Runs necessary functions to start pygame etc.
        """
        self.app_settings, self.workspace_settings, self.camera_settings = self.load_config() # Load the game config
        
        self.load_core() 
        
        pygame.display.set_caption(self.app_settings["window-title-name"])  # Set Window Title

    def load_core(self):
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.elapsed_time = 0
        
        self.viewport = ViewportModule.Viewport(self)
        self.viewport_offset = self.viewport.main_camera.get_camera_offset() # Get the offset from the camera

    def load_services(self):
        
        self.scene_service = SceneService.SceneService(self)
        self.gui_service = GuiService.GuiService(self)
        self.tween_service = TweenService.TweenService(self)
        self.transition_service = TransitionService.TransitionService(self)
        
        if self.workspace_settings["debug-mode"]:
            self.debug_service = DebugService.DebugService(self, self.clock)
        else:
            self.debug_service = None
         
    def send_key(self, key):
        event = pygame.event.Event(pygame.KEYDOWN, key=key)
        pygame.event.post(event)
        

    def run(self):
        fps = self.app_settings["max-fps"]
        
        while True:
            self.events()
            self.update()
            self.draw()
            
            self.delta_time = self.clock.tick(100000) * .001
            self.elapsed_time += self.delta_time            
            
    def qt_run(self):
        """ONLY USE IF YOU INTEND TO USE WITH PYQT5/PYSIDE"""
        fps = self.app_settings["max-fps"]
        
        while True:
            self.events()
            self.update()
            self.draw()
            
            self.delta_time = self.clock.tick(100000) * .001
            self.elapsed_time += self.delta_time         
            
            yield self.get_screen()
            

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            self.event_queue = event
            self.gui_service.handle_event(event, self)
            
            if self.debug_service:
                self.debug_service.handle_event(event)
                
        

    def update(self):
        self.transition_service.update()
        self.scene_service.run_scene(self.event_queue)
        self.tween_service.update(self.delta_time)
       
        if self.debug_service:
            self.debug_service.update()
        

    def draw(self):
        self.scene_service.draw_scene(self.viewport.get_main_camera_surface())
        self.gui_service.draw(self.get_screen(), self.viewport, self.get_current_scene())
        self.viewport.draw()

    def get_gui_service(self):
        return self.gui_service

    def get_main_camera(self):
        return self.scene_service.get_main_camera()

    def get_screen(self):
        return self.viewport.get_screen()
    
    def get_viewport(self):
        return self.viewport
    
    def get_delta_time(self):
        return self.delta_time
    
    def get_elapsed_time(self):
        return self.elapsed_time
    
    def get_fps(self):
        return self.clock.get_fps()
    
    def get_current_scene(self):
        return self.scene_service.get_scene()