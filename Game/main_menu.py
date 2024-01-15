import pytweening, pygame, sys, os
import random

import engine.libs.Formatter as formatter
import engine.libs.Utils as utils
import engine.libs.EntityService as EntityService 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService

class Debugger(EntityService.Entity):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
        
    
    def update(self):
        print("PRITING ENTITY")



class Menu(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        print("Loaded")
        
        #self.testimg = GuiService.Element((200, 200), "test.png")
        self.testbutton = GuiService.ButtonElement((600, 200), "test2.png", "test2.png", self.testbtn, self.testbtn)
    
    def testbtn(self):
        print("clicked")
        self.app.scenes.set_scene("options")

    def on_enter(self):
        return super().on_enter()
     
    def update(self):
        pass
          
    def draw(self):
        self.app.get_screen().fill((255))  
      
class Options(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        print("Loaded")
        
        self.testimg2 = GuiService.Element((800, 200), "test.png")
     
    def on_enter(self):
        return super().on_enter() 
    
    def update(self):
        pass
        
    def draw(self):
        self.app.get_screen().fill((0, 255, 0))
