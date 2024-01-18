import pygame, json, os, sys

import engine.libs.Formatter as formatter
import engine.libs.Utils as utils
import engine.libs.EntityService as EntityService 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService
import engine.libs.TransitionService as TransitionService

class App():
    """
    Main game/app loop class for the PyRed Engine.
    """

   
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        
        global screen, clock, settings
        self.entities, self.scenes, self.guis , self.tweens, self.transitions = self.start_services()

        screen, clock, settings = self.start_game()
        self.event_queue = None
        self.load_scenes()
    
    """
    def load_scenes(self):
        self.scenes.load_scenes()
        self.scenes.set_scene(settings["start-scene"])  
    """
       
    def start_game(self):
        """
        Runs necessary functions to start pygame etc.
        """
        # TODO Add support here for callbacks
        res, fps, caption, icon, settings = self.load_config()
        screen_w, screen_h = formatter.get_dimensions(res)  # Window Height Constants
        
        screen = pygame.display.set_mode((screen_w, screen_h))  # Screen initialisation
        clock = pygame.time.Clock()
        pygame.display.set_caption(caption)  # Set Window Title
        
        if icon:
            pygame.display.set_icon(pygame.image.load(icon))  # Window icon
        
        #---------------------------
        
        
        
        return screen, clock, settings
    def start_services(self):
        entities = EntityService.EntityService()
        scenes = SceneService.SceneService(self) 
        guis = GuiService.GuiService()
        tweens = TweenService.TweenService()
        transitions = TransitionService.TransitionService()

        return entities, scenes, guis, tweens, transitions
         
    def load_config(self):
        """
        Loads game settings from a "config.json" file.
        """
        with open("config.json", "r") as conf:
            data_raw = json.load(conf)
            settings = data_raw["app"]["settings"]
            
            print(settings)
            
            res = settings["resolution"]
            fps = settings["max-fps"]
            caption = settings["window-title-name"]
            icon = settings["window-icon-path"]
            
            if icon == "None" or icon == None or icon == "":
                icon = None    
            return res, fps, caption, icon, settings
           
    def run(self):
        fps = settings["max-fps"]
        
        while True:
            clock.tick(fps)
            delta_time = clock.tick(fps) / 1000.0
            
           
            self.events()
            self.update()
            self.draw()
            
    def events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
                self.event_queue = event
                self.guis.handle_event(event)
                
    def update(self):
        self.transitions.update()
        self.scenes.run_scene(self.event_queue) 
        self.entities.update()
        self.tweens.update()

        print(self.get_clock().get_fps())
    def draw(self):
        self.guis.draw(screen)
        pygame.display.flip()  
          
    def get_screen(self):
        return screen

    def get_clock(self):
        return clock

        
        





