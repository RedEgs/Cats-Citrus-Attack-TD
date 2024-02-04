import pytweening, pygame, sys, os
import sqlite3
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

        self.db_filename = 'credentials.db'
        self.init_database()

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
        
    def init_database(self):
        # Create a connection to the SQLite database
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()

        # Create a table for user credentials if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT
            )
        ''')

        conn.commit()
        conn.close()
     
        
    def sign_up(self):
        new_username = self.username_entry.get_submitted_text()
        new_password = self.password_entry.get_submitted_text()

        try:
            # Insert new user into the 'users' table
            conn = sqlite3.connect(self.db_filename)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (username, password) VALUES (?, ?)
            ''', (new_username, new_password))
            
            conn.commit()
            conn.close()

            self.login_status.update_text("Sign-up Successful!")
            self.login_status.update_color((30, 230, 0))
        except sqlite3.Error as e:
            print(f"Error during sign-up: {e}")
            self.login_status.update_text("Error during sign-up")

        
    def login(self):
        username = self.username_entry.get_submitted_text()
        password = self.password_entry.get_submitted_text()

        status = None

        try:
            # Check credentials in the 'users' table
            conn = sqlite3.connect(self.db_filename)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                print("Login successful!")
                status = True
            else:
                print("Invalid credentials. Please try again.")
                status = False
        except sqlite3.Error as e:
            print(f"Error during login: {e}")
            status = None

        return status
            
        
        
      
