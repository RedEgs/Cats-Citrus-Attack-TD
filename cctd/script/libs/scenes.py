import pygame

class SceneDirector:
    def __init__(self, current_scene):
        self.current_scene = current_scene
        self.scenes = {}

    def load_scenes(self, scenes):
        for scene in scenes:
            name = str(scene.get_scene_info())
            self.scenes.update({str(name): scene})

    def run_scene(self):
        self.current_scene.run()

    def set_scene(self, scene):
        self.current_scene = scene

    def get_scene(self):
        return self.current_scene
    
    def get_loaded_scenes(self):
        return self.scenes

class Scene:
    def __init__(self, screen, scene_director, scene_name):
        self.scene_name = scene_name
        self.sceneDirector = scene_director
        self.screen = screen

    def events(self, event):
        pass                                                     

    def update(self):
        pass

    def draw(self):
        pass

    def run(self):
        self.events()
        self.update()
        self.draw()

    def get_scene_info(self):
        return self.scene_name

