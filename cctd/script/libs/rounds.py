import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.scenes import *
from ..libs.map import *
from ..libs.gui import *
from ..libs.towers import *
from ..libs.shop import *

class RoundDirector():
    def __init__(self, gui_director, screen, scene_director, tween_director, tower_director):
        self.gui_director = GUIDirector()

        self.screen = screen
        self.tween_director = TweenDirector
        self.tower_direcotr = TowerDirector
        
    
    def events(self):
        pass
    
    def draw(self):
        pass
        
    def update(self):
        if tower_director.towers_amount >= 1:
            self.ask_start()
    
    
    def ask_start(self):
        self.play_button = Button(self.gui_director, (self.center_pos[0], self.center_pos[1]+500), os.path.join(current_dir, '..', '..', 'resources', 'main_menu', 'play_button_off.png'), 
                                  os.path.join(current_dir, '..', '..', 'resources', 'main_menu', 'play_button_on.png'), lambda: self.scene_director.switch_scene("lobby_scene"), lambda: None)
        self.play_button_tween = TweenVector2(TweenData((self.center_pos[0], self.center_pos[1]+500), (self.center_pos[0], 330), 2, .5, pytweening.easeInOutCubic), self.tween_director)
        self.play_button_tween.start()
        
    