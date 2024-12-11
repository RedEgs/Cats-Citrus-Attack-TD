# Main project file
import pygame, os, sys
from sys import modules
import importlib
from pyredengine import PreviewMain # type: ignore

import cctd
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

class Main(PreviewMain.MainGame):
    def __init__(self, fullscreen = False) -> None:
        super().__init__(fullscreen, [800, 600])
        """
        Make sure not to remove the super() method above, as it will break the whole script.
        """        
        self.display = pygame.display.get_surface() #sd[UNPACK]
        if self._engine_mode:
            abspath = os.path.abspath(__file__)
            dname = os.path.dirname(abspath)
            os.chdir(dname)
            
        
        self.game_registry = Registry() #[UNPACK]
        
        self.transitionDirector = TransitionDirector(self.display)
        self.SceneDirector = SceneDirector("main_menu", self.display, self.transitionDirector) #[UNPACK]
    
        
    
        game_scenes = []
        game_scenes.append(Menu(self.display, self.SceneDirector, "main_menu"))
        game_scenes.append(LobbyScene(self.display, self.game_registry, self.SceneDirector, "lobby_scene"))
        #game_scenes.append(ExampleScene(self.display, self.SceneDirector, "example_scene"))
        game_scenes.append(EndlessGameScene(self.display, self.game_registry, self.SceneDirector, "game_scene"))



        # Game(self.self.display, self.SceneDirector, "debug_scene")
        self.eventQueue = None
        self.SceneDirector.load_scenes(game_scenes)
        
    


        
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
            self.eventQueue = event
               
    def update(self):
        """
        This is where you independant code goes. 
        This is purely a conceptual seperator from the rest of the game code.
        Think of this as the "body" of your program.
        """
        #self.iterator += 1
        
        self.SceneDirector.run_scene(self.eventQueue)
        self.transitionDirector.update()
        

    def draw(self):
        """
        This is where your drawing code should do.
        Make sure that `pygame.display.flip()` is the last line.
        Make sure that `self.display.fill()` is at the start too.
        """
        pygame.display.flip()
    
    
    def on_reload(self):
        return super().on_reload()