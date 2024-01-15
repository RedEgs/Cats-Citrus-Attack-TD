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
        
        self.app = app
        self.guis = app.guis

        self.tweens = app.tweens
        
        self.testimg = GuiService.Element((200, 200), "test.png")
        self.tween_data = TweenService.TweenDataVector2((500,500), (800,800), 10, 0)
        self.tween = TweenService.TweenVector2(self.tween_data)
        self.text = GuiService.TextElement((500,500), "testicles", 24, (0))
        self.tween.start()
        
            
    def update(self):
        self.tweens.update()
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