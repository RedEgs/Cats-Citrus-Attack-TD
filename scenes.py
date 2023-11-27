import pygame


class SceneDirector:
    def __init__(self, current_scene):
        self.current_scene = current_scene
        self.state = 0

    def switch_scene(self, scene):
        self.state = 1
        self.set_scene(scene)

    def get_scene(self):
        return self.current_scene

    def set_scene(self, scene):
        self.current_scene = scene


class Scene:
    def __init__(self, screen, scene_director):
        self.screen = screen
        self.sceneDirector = scene_director
