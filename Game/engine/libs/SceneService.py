import pygame, json, os, sys

import engine.libs.Utils as utils
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService
import engine.libs.TransitionService as TransitionService

class SceneService():
    """
    Handles the loading, setting, etc., of all scenes
    """
    all_scenes = []

    def __init__(self, app):
        self.app = app

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

    def get_scene_by_name(self, name):
        if name in self.scenes:
            return self.scenes.get(name)
        else:
            return False

    def run_scene(self, event):   
        try:
            self.scenes[self.get_scene()].run(event)
        except KeyError:  
            print("No scene found")

    def draw_scene(self):   
        try:
            self.scenes[self.get_scene()].draw()
        except KeyError:  
            print("No scene found")


    def set_scene(self, scene):
        self.previous_scene = self.active_scene
        self.active_scene = scene


        try:
            self.scenes[self.get_previous_scene()].on_exit()
            self.scenes[self.get_scene()].on_enter()
        except KeyError:
            pass        
        
    def switch_scene(self, scene, *extra_data):
        TransitionService.TransitionService.canTransition = False
        TransitionService.TransitionService.isTransitioning = True

        TransitionService.FadeTransition(self.get_previous_scene(), scene, self.app, 1)
        self.get_scene_by_name(scene).set_extra_data(extra_data)
        
        #.set_extra_data(*extra_data)

        TransitionService.TransitionService.canTransition = True
        TransitionService.TransitionService.isTransitioning = False

    def get_scene_obj(self):
        name = self.get_scene()
        if name in self.scenes:
            return self.scenes.get(name)
        else:
            return False

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
        self.guis = app.guis
        self.guis.set_active_scene(self)

        self.extra_data = None

        self.element_cache = []
        self.event_element_cache = []
        
        self.cached = False
        self.cached_event_element = False

    def on_exit(self):
        pass

    def on_enter(self):
        self.guis.set_active_scene(self)
        print("CHhanged scene")

    def events(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def run(self, event):
        self.events(event)
        self.update()
        #self.draw()

    def get_scene_info(self):
        return self.scene_name
    
    def set_extra_data(self, extra_data):
        self.extra_data = extra_data
        