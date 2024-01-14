import pytweening, pygame, sys, os
import random

import engine.libs.formatter as formatter
import engine.libs.utils as utils
import engine.libs.EntityService as EntityService 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 


class Debugger(EntityService.Entity):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
        
    
    def update(self):
        print("PRITING ENTITY")



class Menu(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        self.debugger = Debugger()
        
        self.app = app
        self.guis = app.guis
        
        self.entities, self.scenes, self.guis = self.app.start_services()
        self.testimg = GuiService.Element((200, 200), "test.png")
            
            
            
    def update(self):
        pass
        #self.debugger.update() 
          
    def draw(self):
        self.app.get_screen().fill((255))
        
        
        self.guis.draw(self.app.get_screen())
        
        
class Options(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
     
    def update(self):
        print("PRITING ENTITY IN OPTIONS")
        
        
    def draw(self):

        self.app.get_screen().fill((0, 255, 0))