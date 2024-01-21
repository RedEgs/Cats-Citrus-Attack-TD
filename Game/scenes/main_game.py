import pytweening, pygame, sys, os
from enum import Enum

import engine.libs.Formatter as formatter
import engine.libs.Utils as utils
import engine.libs.EntityService as EntityService 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService

import cctd.scripts.map_loader as map_loader
import cctd.scripts.enemy_handler as enemy_handler

class GameState(Enum):
    PREROUND = "preround"
    MIDROUND = "midround"
    PAUSED = "paused"
    
    
    
    
class Main_Game(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        self.app = app
        
        
        self.map_handler = map_loader.Map_Loader()
        self.map = self.map_handler.load_map()
        self.map_index = 1
        self.map_surface = GuiService.SurfaceElement((formatter.get_center(1280, 720)), self.map.map_image) # Background
        
        self.game_state = GameState.PREROUND
        self.start_button = None
        
        self.enemy_handler = enemy_handler.EnemyHandler()
        
    
    
      

    def on_enter(self):
        super().on_enter()    
        
        self.map_index = self.extra_data[0]

        self.map_surface.update_surface(self.map.load_map()[0])
        
        self.start_button = GuiService.ButtonElement((300, 300), ["cctd/resources/main_menu/play_button.png"], [self.start_game])
        
        
     
    def update(self):
        self.enemy_handler.update()
        
        if self.game_state == GameState.MIDROUND:
            pass

            
            
            
  
    def draw(self):
        self.app.get_screen().fill((0))  
        self.enemy_handler.draw(self.app.get_screen())
       
       
      
    def start_game(self):
        self.game_state = GameState.MIDROUND
        
        tween_data = TweenService.TweenDataVector2((30,30), (-30,-30), .5, 0)
        tween = TweenService.TweenVector2(tween_data)
        
        self.start_button.update_position(tween.get_output())
        
        enemy = enemy_handler.Enemy(self.map.waypoint_data)
