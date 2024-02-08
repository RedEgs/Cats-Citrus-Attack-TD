import pytweening, pygame, sys, os

import engine.libs.Formatter as formatter
import engine.libs.Utils as utils
import engine.libs.EntityService as EntityService 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService

class FPSCounter(GuiService.TextElement):
    def __init__(self, position, text, size, color):
        super().__init__(position, text, size, color)

    def update_position(self, position):
        return super().update_position(position)
    
    def update_text(self, text):
        return super().update_text(text)
    
    def draw(self, screen):
        return super().draw(screen)
    




class DebugService():
    def __init__(self, app, clock):
        self.app = app
        self.clock = clock

        self.fps = FPSCounter((40,40), str(round(self.clock.get_fps(), 0)), 24, (255, 255, 255))

    def update(self):
        self.fps.update_text(str(round(self.clock.get_fps(), 0)))


    def draw(self, screen):
        self.fps.draw(screen)