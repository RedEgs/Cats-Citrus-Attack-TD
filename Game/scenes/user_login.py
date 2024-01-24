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

        self.username_entry = GuiService.TextArea((246, 279), "Username", "cctd/resources/user_login/text_enter.png")
        self.password_entry = GuiService.TextArea((246, 366), "Password", "cctd/resources/user_login/text_enter.png")

        self.login_button = GuiService.ButtonElement((257, 537), ["cctd/resources/user_login/login_button.png"], [None])
        self.signup_button = GuiService.ButtonElement((169, 625), ["cctd/resources/user_login/sign_up_button.png"], [None])
        self.continue_button = GuiService.ButtonElement((346, 626), ["cctd/resources/user_login/continue_button.png"], [self.contine_to_menu])

    def draw(self):
        self.app.get_screen().fill((0))  
    
    def contine_to_menu(self):
        self.app.scenes.switch_scene("main_menu")
        
      
