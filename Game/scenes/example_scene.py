import pytweening, pygame, sys, os
import asyncio

from engine.app import *
from engine.libs import SceneService as SceneService


class Example_Scene(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)

        GuiService.TextElement((100, 100), "Hello world", 24, (255,0,0))
        
    def on_enter(self):
        print("entered")
       
        
    def draw(self):
        self.app.get_screen().fill((255))  
        
      
