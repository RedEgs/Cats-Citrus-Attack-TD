import random, pygame, json, os, sys


import engine.libs.EntityService as EntityService
import engine.libs.SceneService as SceneService
import engine.libs.GuiService as GuiService
import engine.libs.TweenService as TweenService
import engine.libs.TransitionService as TransitionService
import engine.libs.DebugService as DebugService
import engine.libs.CameraService as CameraService


class App:
    """
    Main game/app loop class for the PyRed Engine.
    """

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        global camera, display, screen, clock, settings

        camera, clock, settings = self.start_game()

        screen = camera.get_screen()
        display = camera.get_display()
        self.camera_offset = camera.get_camera_offset()

        (
            self.entities,
            self.scenes,
            self.guis,
            self.tweens,
            self.transitions,
            self.debugs,
        ) = self.start_services()

        self.load_scenes()
        self.guis.load_scene_elements()

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
        entities = EntityService.EntityService()
        scenes = SceneService.SceneService(self)
        guis = GuiService.GuiService()
        tweens = TweenService.TweenService()
        transitions = TransitionService.TransitionService()
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

        while True:
            self.events()
            self.update()
            self.draw()

            clock.tick(fps)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.event_queue = event
            self.guis.handle_event(event, self.get_camera())
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
