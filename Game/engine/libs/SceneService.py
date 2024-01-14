import pygame, json, os, sys

class SceneService():
    """
    Handles the loading, setting, etc., of all scenes
    """
    all_scenes = []

    def __init__(self):
        self.active_scene = None
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
            self.all_scenes.append(scene)

    def run_scene(self, event):   
        try:
            self.scenes[self.get_scene()].run(event)
        except KeyError:  
            print("No scene found")

    def set_scene(self, scene):
        self.previous_scene = self.active_scene
        self.active_scene = scene


        try:
            self.scenes[self.get_previous_scene()].on_exit()
        except KeyError:
            pass        
        
        #self.scenes[self.get_scene()].on_enter()

    def get_previous_scene(self):
        return self.previous_scene

    def get_scene(self):
        return self.active_scene

    def get_loaded_scenes(self):
        return self.scenes


class Scene():
    def __init__(self, scene_name, app):
        self.scene_name = scene_name
        SceneService.all_scenes.append(self)
        
        self.app = app
        

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