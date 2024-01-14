import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.utils import *
from ..libs.scenes import *

class Options(Scene):
    def __init__(self, screen, scene_director, scene_name):
        super().__init__(screen, scene_director, scene_name)

        self.screen = screen
        self.sceneDirector = scene_director
        self.scene_name = scene_name
        
    def on_exit(self):
        return super().on_exit()

    def on_enter(self):
        return super().on_enter()



        
    
    def events(self, event):
        return super().events(event)

    def update(self):
        return super().update()

    def draw(self):
        return super().draw()

    def run(self, event):
        self.events(event)
        self.update()
        self.draw()

    def get_scene_info(self):
        return self.scene_name
