import pytweening, pygame, sys, os
from enum import Enum

import engine.libs.Maths as Maths
import engine.libs.Utils as utils
 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService

import cctd.scripts.map_loader as map_loader
import cctd.scripts.enemy_handler as enemy_handler
import cctd.scripts.tower_handler as tower_handler

class GameState(Enum):
    PREROUND = "preround"
    MIDROUND = "midround"
    PAUSED = "paused"
    
class PlayerMenuState(Enum):
    NONE = "none",
    PLACING = "placing",
    

class Main_Game(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        self.app = app
        
        self.map_handler = map_loader.Map_Loader()
        self.map = self.map_handler.load_map()
        self.map_index = 1
        self.map_surface = GuiService.SurfaceElement((Maths.get_center(1280, 720)), self.map.map_image) # Background
        
        self.player_menu_state = PlayerMenuState.NONE
        self.game_state = GameState.PREROUND
        self.start_button = None
        
        self.build_mode_button = GuiService.ButtonElement((60, 60), ["cctd/resources/gameplay_overlays/build_mode_button.png"], [self.enter_build_mode])
        self.exit_mode_button = GuiService.ButtonElement((-60,-60), ["cctd/resources/gameplay_overlays/exit_mode_button.png"], [self.exit_build_mode])

        self.enemy_handler = enemy_handler.EnemyHandler()
        self.tower_handler = tower_handler.TowerHandler(app, self.map)


    def on_enter(self):
        super().on_enter()    
        
        self.map_index = self.extra_data[0]

        self.map_surface.update_surface(self.map.load_map()[0])
        
        #self.start_button = GuiService.ButtonElement((300, 300), ["cctd/resources/main_menu/play_button.png"], [self.start_game])
        

        
    def events(self, event):
        #self.tower_handler.handle_event(event)
        pass

    def update(self):
        self.enemy_handler.update()
        self.tower_handler.update()
        
        if self.game_state == GameState.MIDROUND:
            pass

        
      
        if self.player_menu_state == PlayerMenuState.NONE:
            self.tween_data = TweenService.TweenDataVector2((-60, -60), (60, 60), 1, 0)
            self.tween = TweenService.TweenVector2(self.tween_data)
            self.tween.start()

            self.tween_data2 = TweenService.TweenDataVector2((60, 60), (-60, -60), 1, 0)
            self.tween2 = TweenService.TweenVector2(self.tween_data2)
            self.tween2.start()
        elif self.player_menu_state == PlayerMenuState.PLACING:
            self.tween.reverse()
            self.tween2.reverse()

        self.build_mode_button.update_position(self.tween.get_output())
        self.exit_mode_button.update_position(self.tween2.get_output())
  
    def draw(self):
        self.enemy_handler.draw(self.app.get_screen())
        self.tower_handler.draw(self.app.get_screen())

    def start_game(self):
        self.game_state = GameState.MIDROUND
        
        tween_data = TweenService.TweenDataVector2((30,30), (-30,-30), .5, 0)
        tween = TweenService.TweenVector2(tween_data)
        
        self.start_button.update_position(tween.get_output())
        
        enemy = enemy_handler.Enemy(self.map.waypoint_data)

    def enter_build_mode(self):
        self.player_menu_state = PlayerMenuState.PLACING

    def exit_build_mode(self):
        self.player_menu_state = PlayerMenuState.NONE
