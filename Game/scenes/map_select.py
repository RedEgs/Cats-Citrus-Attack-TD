import pytweening, pygame, sys, os

import engine.libs.Formatter as formatter
import engine.libs.Utils as utils
import engine.libs.EntityService as EntityService 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService


class Map_Select(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        self.app = app

        GuiService.ImageElement((formatter.get_center(1280, 720)), "cctd/resources/map_select/background.png") # Background

        back_button = GuiService.ButtonElement((98, 70), ["cctd/resources/map_select/back_button.png"], [self.back_button])

        left_button = GuiService.ButtonElement((342, 572), ["cctd/resources/map_select/left_button.png"], [self.back_button])
        right_button = GuiService.ButtonElement((477, 577), ["cctd/resources/map_select/right_button.png"], [self.back_button])
        map_preview = GuiService.ImageElement((421, 314), "cctd/resources/map_select/map_preview.png")
        
        continue_button = GuiService.ButtonElement((1060, 606), ["cctd/resources/map_select/continue_button.png"], [self.continue_button])

    def back_button(self):
        self.app.scenes.switch_scene("main_menu")
    
    def continue_button(self):
        self.app.scenes.switch_scene("main_game")
    
    
    def on_enter(self):
        super().on_enter()
     
    def update(self):
        pass
        
    def draw(self):
        self.app.get_screen().fill((0))  
      
