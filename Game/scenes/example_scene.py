import pytweening, pygame, sys, os
import ctypes
from ctypes import wintypes

from engine.app import *
from engine.libs import SceneService as SceneService
from engine.libs import Maths


class Example_Scene(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        self.app = app
        self.camera = self.app.get_camera()

        # All Normal GUI Elements

        # GuiService.TextElement(
        #     GuiService.GuiSpaces.SCREEN,
        #     self.camera,
        #     (800, 100),
        #     "tETS tETX blox",
        #     24,
        #     (0, 0, 0),
        #     "left",
        # )
        #self.img = GuiService.ImageElement(GuiService.GuiSpaces.WORLD, self.camera, (0,0),"test_image.png")
        
        # GuiService.StatusBar(GuiService.GuiSpaces.SCREEN, self.camera, (100, 400), (100, 50), initial_value=10)
        
        # GuiService.EasyCurve(GuiService.GuiSpaces.SCREEN, self.camera, (100,100), (200, 200))
        
        
        # All Event Elements
        # GuiService.TextInput(GuiService.GuiSpaces.SCREEN, self.camera, (700, 200), 24, "test input")
        # GuiService.Slider(GuiService.GuiSpaces.SCREEN, self.camera, (200, 300), (100, 25))
        # GuiService.Checkbox(GuiService.GuiSpaces.SCREEN, self.camera, (100, 300))
        # GuiService.ButtonElement(GuiService.GuiSpaces.SCREEN, self.camera, (300, 200))
        #self.rect = GuiService.DraggableRect(GuiService.GuiSpaces.WORLD, self.camera, (-50, 100), (0, 0, 255), (100, 100))
        
    
    def update(self):
        pass
        # print(f"world pos: {self.rect.world_position}")
        # print(f"screen pos: {self.rect.screen_position}")

    def events(self, event):
        # if event.type == self.camera.camera_event:
        #     print(self.camera.camera_offset)
        pass

    def draw(self, screen):
        #screen.fill((235, 235, 235))
        screen.fill((35, 35, 35))