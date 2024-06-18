
import pytweening, pygame, sys, os
from enum import Enum

import engine.libs.Formatter as formatter
import engine.libs.Utils as utils
 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService
import engine.libs.NetworkService as NetworkService


class Network_Test(SceneService.Scene):
    def __init__(self, scene_name, app):# Background
        super().__init__(scene_name, app)
        self.app = app

        self.host_button = GuiService.ButtonElement(formatter.get_center(1280, 720), ["cctd/resources/main_menu/play_button.png"], [self.host_server, self.connect_server])

        self.ip = GuiService.TextArea((800, 500), "IP", "cctd/resources/user_login/text_enter.png")
        self.port = GuiService.TextArea((800, 700), "PORT", "cctd/resources/user_login/text_enter.png")
        

        #self.text_status = GuiService.TextElement((formatter.get_center(1280, 720-90)), "Not connected", 24, (255,0,0))

    def host_server(self):
       print("ran server")
       self.server =  NetworkService.Server(self.ip.get_submitted_text(), int(self.port.get_submitted_text()))
    
    def connect_server(self):
        print("ran client")
        self.client = NetworkService.Client(self.ip.get_submitted_text(), int(self.port.get_submitted_text()))

    def draw(self):
        self.app.get_screen().fill((255,255,255))  

        
    def on_enter(self):
        super().on_enter()
     
    def update(self):
        try:
            self.server.run()
        except AttributeError:
            pass
        
        try:
            self.client.run()
        except AttributeError:
            pass
        