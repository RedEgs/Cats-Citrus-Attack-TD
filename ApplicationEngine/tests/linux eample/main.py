# Main project file
import pygame, os, sys
from pyredengine import PreviewMain # type: ignore

from cctd.script.libs.scenes import *
from cctd.script.libs.utils import *
from cctd.script.libs.transitions import *
from cctd.script.libs.registry import *

from cctd.script.scenes.example import ExampleScene
from cctd.script.scenes.menu import Menu
from cctd.script.scenes.lobby import LobbyScene
from cctd.script.scenes.game import EndlessGameScene



"""
All code given is the bare minimum to safely run code within the engine.
Removing any code that already exists in not recommended and you WILL run into issues.
When compiled, parts of code are removed to optimise and simplify the file.
"""



class cctd:
    def __init__(self, screen):
        self.game_registry = Registry()
        
        self.transitionDirector = TransitionDirector(screen)
        self.SceneDirector = SceneDirector("main_menu", screen, self.transitionDirector)

    
        game_scenes = []
        game_scenes.append(Menu(screen, self.SceneDirector, "main_menu"))
        game_scenes.append(LobbyScene(screen, self.game_registry, self.SceneDirector, "lobby_scene"))
        #game_scenes.append(ExampleScene(screen, self.SceneDirector, "example_scene"))
        game_scenes.append(EndlessGameScene(screen, self.game_registry, self.SceneDirector, "game_scene"))

        # Game(self.SCREEN, self.SceneDirector, "debug_scene")
        self.SceneDirector.load_scenes(game_scenes)
   

    def run(self):
        self.game_registry.load_tower_registry()
        self.events()
        self.update()
        self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.eventQueue = event

    def update(self):
        self.SceneDirector.run_scene(self.eventQueue)
        self.transitionDirector.update()

    def draw(self):
        pygame.display.flip()

class Main(PreviewMain.MainGame):
    def __init__(self, fullscreen = False) -> None:
        super().__init__(fullscreen)
        """
        Make sure not to remove the super() method above, as it will break the whole script.
        """

        self.display = pygame.display.get_surface()
        if self._engine_mode:
            abspath = os.path.abspath(__file__)
            dname = os.path.dirname(abspath)
            os.chdir(dname)
        
        self.cctd = cctd(self.display)
        
        
    


        
    def handle_events(self): 
        """
        All your logic for handling events should go here. 
        Its recommended you write code to do with event handling here.
        Make sure that you don't remove the `pygame.QUIT` event as the game won't be able to be shutdown.
        See pygame docs for more info: https://www.pygame.org/docs/ref/event.html.
        """
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
               
    def update(self):
        """
        This is where you independant code goes. 
        This is purely a conceptual seperator from the rest of the game code.
        Think of this as the "body" of your program.
        """
        self.cctd.run()

    def draw(self):
        """
        This is where your drawing code should do.
        Make sure that `pygame.display.flip()` is the last line.
        Make sure that `self.display.fill()` is at the start too.
        """
        pygame.display.flip()
    
    
