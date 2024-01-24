import pytweening, pygame, sys, os
from enum import Enum

import engine.libs.Formatter as formatter
import engine.libs.Utils as utils
import engine.libs.EntityService as EntityService 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService

class User_Login(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        GuiService.ImageElement((formatter.get_center(1280, 720)), "cctd/resources/user_login/background.png") # Background
        GuiService.ImageElement((236, 163), "cctd/resources/user_login/logo.png")

        self.username = GuiService.TextArea((246, 279), "Username", "cctd/resources/user_login/text_enter.png")
        self.password = GuiService.TextArea((246, 366), "Password", "cctd/resources/user_login/text_enter.png")


    def draw(self):
        self.app.get_screen().fill((0))  
      
