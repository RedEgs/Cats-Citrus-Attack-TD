import pygame, json, os, sys

from engine.app import *
from engine.libs import SceneService as SceneService

import scenes.main_menu as main_menu

class Main(App):
    def __init__(self):
        super().__init__()

    def load_scenes(self):
        self.scenes.load_scenes([main_menu.Menu("main_menu", self)])
        self.scenes.set_scene("main_menu")  
         
        
        

        
        
        

    

if __name__ == "__main__":
    main = Main()
    main.run()
