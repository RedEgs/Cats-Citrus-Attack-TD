import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.utils import *
from ..libs.scenes import *
from ..libs.transitions import *

class SceneDirector:
    def __init__(self, current_scene, screen, transition_director):
        self.screen = screen
        self.transition_director = transition_director
        self.current_scene = current_scene
        self.previous_scene = None
        self.scenes = {}

    def enter_scene(self):
        pass

    def exit_scene(self):
        pass

    def load_scenes(self, scenes):
        for scene in scenes:
            name = str(scene.get_scene_info())
            self.scenes.update({str(name): scene})

    def switch_scene(self, scene):
        FadeTransition(self.screen, self, self.transition_director, self.get_previous_scene(), scene, 1)
        
    def run_scene(self, event):
        self.scenes[self.get_scene()].run(event)

    def set_scene(self, scene): # Changes the currently running game scene
        self.previous_scene = self.current_scene # Sets the previous scene to the current scene
        self.current_scene = scene # Then sets the current scene to the new scene

        self.scenes[self.get_previous_scene()].on_exit()
        self.scenes[self.get_scene()].on_enter()

    def get_previous_scene(self):
        return self.previous_scene    

    def get_scene(self):
        return self.current_scene

    def get_loaded_scenes(self):
        return self.scenes


class Scene:
    def __init__(self, screen, scene_director, scene_name):
        self.scene_name = scene_name
        self.sceneDirector = scene_director
        self.screen = screen


    def on_exit(self):
        pass

    def on_enter(self):
        pass

    def events(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def run(self, event):
        self.events(event)
        self.update()
        self.draw()

    def get_scene_info(self):
        return self.scene_name
