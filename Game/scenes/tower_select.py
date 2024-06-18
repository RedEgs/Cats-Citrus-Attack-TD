import pytweening, pygame, sys, os

import engine.libs.Formatter as formatter
import engine.libs.Utils as utils
 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService


class Tower_Select(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        self.app = app

        GuiService.ImageElement((formatter.get_center(1280, 720)), "cctd/resources/tower_select/background.png") # Background

        start_button = GuiService.ButtonElement((988, 592), ["cctd/resources/tower_select/start_button.png"], [self.start_button])

    def back_button(self):
        self.app.scenes.switch_scene("main_menu")
    
    def start_button(self):
        self.app.scenes.switch_scene("main_menu")
    
    
    def on_enter(self):
        super().on_enter()
     
    def update(self):
        pass
        
    def draw(self):
        pass
      
