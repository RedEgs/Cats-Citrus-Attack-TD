import pytweening, pygame, sys, os

import engine.libs.Formatter as formatter
import engine.libs.Utils as utils
import engine.libs.EntityService as EntityService 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService

import cctd.scripts.map_loader as map_loader
class Map_Select(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        self.app = app

        self.map_handler = map_loader.Map_Loader()
        self.map = self.map_handler.load_map()
        self.map_image = self.map.map_image

        GuiService.ImageElement((formatter.get_center(1280, 720)), "cctd/resources/map_select/background.png") # Background

        back_button = GuiService.ButtonElement((98, 70), ["cctd/resources/map_select/back_button.png"], [self.back_button])

        left_button = GuiService.ButtonElement((342, 572), ["cctd/resources/map_select/left_button.png"], [self.left_button])
        right_button = GuiService.ButtonElement((477, 577), ["cctd/resources/map_select/right_button.png"], [self.right_button])
        
        self.map_preview = GuiService.SurfaceElement((421, 314), self.map_image,(666,356))
        map_preview_border = GuiService.ImageElement((421, 314), "cctd/resources/map_select/map_preview.png")
        


        continue_button = GuiService.ButtonElement((1060, 606), ["cctd/resources/map_select/continue_button.png"], [self.continue_button])

    def left_button(self):
        if self.map_handler.map_index > 1:
            self.map_handler.map_index -= 1

            self.map = self.map_handler.load_map()
            self.map_image = self.map.map_image

            self.map_preview.update_surface(self.map_image)
        else:
            pass

    

    def right_button(self):
        
        if self.map_handler.map_index >= self.map_handler.max_maps:
            pass
        else:
            self.map_handler.map_index += 1

            self.map = self.map_handler.load_map()
            self.map_image = self.map.map_image

            self.map_preview.update_surface(self.map_image)

    def back_button(self):
        self.app.scenes.switch_scene("main_menu")
    
    def continue_button(self):
        self.app.scenes.switch_scene("main_game", self.map_handler.map_index)
    
    
    def on_enter(self):
        super().on_enter()
     
    def update(self):
        pass
        
    def draw(self):
        pass
