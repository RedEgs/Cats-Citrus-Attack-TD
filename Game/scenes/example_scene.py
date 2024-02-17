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

        GuiService.TextElement(
            GuiService.GuiSpaces.WORLD,
            self.camera,
            (800, 100),
            "tETS tETX blox",
            24,
            (0, 0, 0),
            "left",
        )
        
        GuiService.ImageElement(GuiService.GuiSpaces.WORLD, self.camera, (400,400),"test_image.png")
        
        GuiService.StatusBar(GuiService.GuiSpaces.WORLD, self.camera, (100, 400), (100, 50), initial_value=10)
        
        GuiService.EasyCurve(GuiService.GuiSpaces.WORLD, self.camera, (100,100), (200, 200))
        
        
        # All Event Elements
        GuiService.TextInput(GuiService.GuiSpaces.WORLD, self.camera, (700, 200), 24, "test input")
        GuiService.Slider(GuiService.GuiSpaces.WORLD, self.camera, (200, 300), (100, 25))
        GuiService.Checkbox(GuiService.GuiSpaces.WORLD, self.camera, (100, 300))
        GuiService.ButtonElement(GuiService.GuiSpaces.WORLD, self.camera, (300, 200))
        GuiService.DraggableRect(GuiService.GuiSpaces.WORLD, self.camera, (700, 600), (0, 0, 255), (100, 100))
        
        
        

    def events(self, event):
        # if event.type == self.camera.camera_event:
        #     print(self.camera.camera_offset)
        pass

    def draw(self, screen):
        screen.fill((235, 235, 235))
