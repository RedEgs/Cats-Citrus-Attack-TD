import pytweening, pygame, sys, os

import engine.libs.Formatter as formatter
import engine.libs.Utils as utils
import engine.libs.EntityService as EntityService 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService

class Difficulty_Select(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        self.app = app

        GuiService.ImageElement((formatter.get_center(1280, 720)), "cctd/resources/difficulty_select/background.png") # Background

        back_button = GuiService.ButtonElement((98, 70), ["cctd/resources/difficulty_select/back_button.png"], [self.back_button])

        easy_button = GuiService.ButtonElement((248, 341), ["cctd/resources/difficulty_select/easy_button.png"], [self.back_button])
        medium_button = GuiService.ButtonElement((488, 341), ["cctd/resources/difficulty_select/medium_button.png"], [self.back_button])
        hard_button = GuiService.ButtonElement((741, 341), ["cctd/resources/difficulty_select/hard_button.png"], [self.back_button])
        impossible_button = GuiService.ButtonElement((1002, 341), ["cctd/resources/difficulty_select/impossible_button.png"], [self.back_button])

        continue_button = GuiService.ButtonElement((640, 600), ["cctd/resources/difficulty_select/continue_button.png"], [self.continue_button])

    def back_button(self):
        self.app.scenes.switch_scene("main_menu")
    
    def continue_button(self):
        self.app.scenes.switch_scene("map_select")
    
    
    
    
    
    
    
    
    def on_enter(self):
        super().on_enter()
     
    def update(self):
        pass
        
    def draw(self):
        pass
        #self.app.get_screen().fill((0))  
      
