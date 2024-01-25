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
        GuiService.ImageElement((246, 163), "cctd/resources/user_login/logo.png")

        self.username_entry = GuiService.TextArea((246, 279), "Username", "cctd/resources/user_login/text_enter.png")
        self.password_entry = GuiService.TextAreaPassword((246, 366), "Password", "cctd/resources/user_login/text_enter.png")

        self.login_button = GuiService.ButtonElement((246, 530), ["cctd/resources/user_login/login_button.png"], [self.check_credentials])
        self.signup_button = GuiService.ButtonElement((158, 626), ["cctd/resources/user_login/sign_up_button.png"], [self.sign_up])
        self.continue_button = GuiService.ButtonElement((336, 626), ["cctd/resources/user_login/continue_button.png"], [self.contine_to_menu])

        self.login_status = GuiService.TextElement((246, 440), "", 24, (255,0,0))

    def draw(self):
        self.app.get_screen().fill((0))  
    
    def contine_to_menu(self):
        self.app.scenes.switch_scene("main_menu")
     
    def check_credentials(self):
        login_data = self.login()
        
        if login_data == True:
            self.contine_to_menu()
        elif login_data == False:
            self.login_status.update_text("Invalid Password or Username")
        elif login_data == None:
            self.login_status.update_text("Login details not found, please signup")
        
          
     
        
    def sign_up(self):
        import json 
        
        new_username = self.username_entry.get_submitted_text()
        new_password = self.password_entry.get_submitted_text()
        
        try:
            with open('credentials.json', 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data[new_username] = new_password

        with open('credentials.json', 'w') as file:
            json.dump(data, file)
            self.login_status.update_text("Sign-up Successful!")
            self.login_status.update_color((30,230,0))
        
    def login(self):
        import json 
        
        username = self.username_entry.get_submitted_text()
        password = self.password_entry.get_submitted_text()
        
        status = None
        
        try:
            with open('credentials.json', 'r') as file:
                data = json.load(file)

            if data.get(username) == password:
                print("Login successful!")
                status = True
            else:
                print("Invalid credentials. Please try again.")
                status = False
        except (FileNotFoundError, json.JSONDecodeError):
            print("No credentials found. Please sign up.")
            status = None
            
        return status
            
        
        
      
