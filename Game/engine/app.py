import logging, random, pygame, json, os, sys
from colorama import Fore, Back, Style

import engine.libs.EntityService as EntityService
import engine.libs.SceneService as SceneService
import engine.libs.GuiService as GuiService
import engine.libs.TweenService as TweenService
import engine.libs.TransitionService as TransitionService
import engine.libs.DebugService as DebugService
import engine.libs.CameraService as CameraService
 
class EngineLogger:
    def __init__(self):
        logging.basicConfig(filename="recent.log", filemode="w", 
                            format="%(asctime)s | %(levelname)s - %(message)s",                            
                            level=logging.INFO)
        self.engine_logger = logging.getLogger()
        logging.info("Initialised the logger!")
        
        
class App:
    """
    Main game/app loop class for the PyRed Engine.
    """

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.engine_logger = EngineLogger().engine_logger


        self.service_registry = []
        self.start_game()

        self.screen = self.camera.get_screen() # Get the screen from the camera
        self.display = self.camera.get_display() # Get the display from camera
        self.camera_offset = self.camera.get_camera_offset() # Get the offset from the camera

        # (
        #     self.entity_service,
        #     self.scene_service,
        #     self.gui_service,
        #     self.tween_service,
        #     self.transition_service,
        #     self.debug_service,
        # ) = self.start_services()
        
        self.start_services()
       

        self.load_scenes()
        self.gui_service.load_scene_elements()

        self.previous_fps = self.clock.get_fps()
        self.fps_high = self.previous_fps
        self.fps_low = 100
        self.current_fps = 0


    def load_config(self):
        """
        Loads game settings from a "config.json" file.
        """

        # Settings Pygame settings (Not related to those in the .json)
        pygame.key.set_repeat(500, 10)
        
        
        with open("config.json", "r") as conf:
            data_raw = json.load(conf)
            
            app_settings = data_raw["app"]["settings"]
            workspace_settings = data_raw["workspace"]["settings"]
            
            # res = settings["resolution"]
            # fps = settings["max-fps"]
            # caption = settings["window-title-name"]
            # icon = settings["window-icon-path"]

            # if icon == "None" or icon is None or icon == "":
            #     icon = None
                
            return app_settings, workspace_settings

    def start_game(self):
        """
        Runs necessary functions to start pygame etc.
        """
        self.app_settings, self.workspace_settings = self.load_config() # Load the game config
        
        self.camera = CameraService.Camera(self, self.app_settings["resolution"], False)
        pygame.display.set_caption(self.app_settings["window-title-name"])  # Set Window Title
        self.clock = pygame.time.Clock()

        # if self.app_settings["icon"]:
        #     pygame.display.set_icon(pygame.image.load(icon))  # Window icon

        # ---------------------------

    def start_services(self):
        
        self.entity_service = EntityService.EntityService(self)
        self.scene_service = SceneService.SceneService(self)
        self.gui_service = GuiService.GuiService(self)
        self.tween_service = TweenService.TweenService(self)
        self.transition_service = TransitionService.TransitionService(self)
        
        if self.workspace_settings["debug-mode"] == True:
            self.debug_service = DebugService.DebugService(self, self.clock)
        else:
            self.debug_service = None
        
        
        
        


    def run(self):
        fps = self.app_settings["max-fps"]
        while True:
            self.events()
            self.update()
            self.draw()

            self.clock.tick()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.event_queue = event
            self.gui_service.handle_event(event, self.get_camera())
            self.get_camera().events(event)
            
            if self.debug_service:
                self.debug_service.handle_event(event)

    def update(self):
        self.transition_service.update()
        self.scene_service.run_scene(self.event_queue)
        self.tween_service.update()
       
        if self.debug_service:
            self.debug_service.update()
        
 
        #self.entity_service.update() # TBA later

    def debug_fps_info(self):      
        self.current_fps = self.clock.get_fps()
        
        if self.current_fps > self.fps_high:
            self.fps_high = self.current_fps
                
        if self.current_fps < self.fps_low and self.current_fps != 0:
            self.fps_low = self.current_fps
            
        print(f"Current: {round(self.current_fps)} | High: {round(self.fps_high)} | Low: {round(self.fps_low)}")
         


    def draw(self):
        self.scene_service.draw_scene(self.display)
        self.gui_service.draw(self.camera)
        self.transition_service.draw(self.display)
        self.camera.draw()
        
        self.debug_fps_info()

    def get_gui_service(self):
        return self.gui_service

    def get_camera(self):
        return self.camera
