
import pytweening, pygame, sys, os
from pygame.locals import *

import engine.libs.Formatter as formatter
import engine.libs.Utils as utils
import engine.libs.EntityService as EntityService 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService



class Map_Editor(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        self.app = app
        
        self.clicked = False
        
        
    def plotlines(self):
        pygame.draw.lines(self.map.map_image, (255,0,0), False, self.map.waypoint_data)

        for waypoint in self.map.waypoint_data:
            pygame.draw.circle(self.map.map_image, (0, 255, 0), waypoint, 5, 5)

    def on_enter(self):
        super().on_enter()    
        self.map = self.extra_data[0]

        GuiService.SurfaceElement((formatter.get_center(1280, 720)), self.map.map_image) # Background
    
    def events(self, event):
        pass
        
        
      
    def update(self):
        pass
        
    def draw(self):
        self.plotlines()
      
