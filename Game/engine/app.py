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

        global camera, display, screen, clock, settings
        camera, clock, settings = self.start_game()

        screen = camera.get_screen()
        display = camera.get_display()
        self.camera_offset = camera.get_camera_offset()

        print(Fore.CYAN + "[3/8] Starting Services...")
        (
            self.entities,
            self.scenes,
            self.guis,
            self.tweens,
            self.transitions,
            self.debugs,
        ) = self.start_services()


        print(Fore.LIGHTGREEN_EX + "[4/8] Completed Services")

        print(Fore.CYAN + "[5/8] Loading Scenes")
        self.load_scenes()
        print(Fore.LIGHTGREEN_EX + "[6/8] Loaded Scenes")

        print(Fore.CYAN + "[7/8] Loading GUI Elements")
        self.guis.load_scene_elements()
        print(Fore.LIGHTGREEN_EX + "[8/8] Loaded GUI Elements")

    def start_game(self):
        """
        Runs necessary functions to start pygame etc.
        """
        res, fps, caption, icon, settings = self.load_config()
        camera = CameraService.Camera(self, res, False)
        clock = pygame.time.Clock()
        pygame.display.set_caption(caption)  # Set Window Title

        if icon:
            pygame.display.set_icon(pygame.image.load(icon))  # Window icon

        # ---------------------------

        return camera, clock, settings

    def start_services(self):
        entities = EntityService.EntityService(self)
        scenes = SceneService.SceneService(self)
        guis = GuiService.GuiService(self)
        tweens = TweenService.TweenService(self)
        transitions = TransitionService.TransitionService(self)
        debugs = DebugService.DebugService(self, clock)

        return entities, scenes, guis, tweens, transitions, debugs

    def load_config(self):
        """
        Loads game settings from a "config.json" file.
        """

        pygame.key.set_repeat(500, 10)
        with open("config.json", "r") as conf:
            data_raw = json.load(conf)
            settings = data_raw["app"]["settings"]

            res = settings["resolution"]
            fps = settings["max-fps"]
            caption = settings["window-title-name"]
            icon = settings["window-icon-path"]

            if icon == "None" or icon is None or icon == "":
                icon = None
            return res, fps, caption, icon, settings

    def run(self):
        fps = settings["max-fps"]
        print("started loop")
        while True:
            self.events()
            self.update()
            self.draw()

            clock.tick()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.event_queue = event
            self.guis.handle_event(event, self.get_camera())
            self.debugs.handle_event(event)
            self.get_camera().events(event)

    def update(self):
        self.transitions.update()
        self.scenes.run_scene(self.event_queue)
        self.entities.update()
        self.tweens.update()
        self.debugs.update()

    def draw(self):
        self.scenes.draw_scene(display)
        self.guis.draw(camera)
        self.transitions.draw(display)
        camera.draw()

    def get_gui_service(self):
        return self.guis

    def get_camera(self):
        return camera
