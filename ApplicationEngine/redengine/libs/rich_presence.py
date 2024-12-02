from pypresence import Presence
from functools import wraps
import time, threading


class RichPresenceHandler():
    def __init__(self):
        self.client_id = "1312502880233853079"
        self.rpc = Presence(self.client_id)  # Initialize the client class
        
        try:
            self.rpc.connect() # Start the handshake loop
            self.connected = True
        except:
            self.connected = False

        self.start_time = time.time()
        self.play_start = 0

    def launcher_state(self):
        if not self.connected:
            return 

        self.rpc.update(
            small_image="launcher_icon_background", small_text="Inside the launcher", 
            large_image="main_icon", large_text="RedEngine", start=self.start_time,
            buttons=[{"label": "Visit Website", "url": "https://www.redegs.world/portfolio"}, {"label": "GitHub", "url": "https://github.com/RedEgs"}],
            details="Inside of the launcher", state="In The Launcher"
        ) # Set the presence

    def engine_state(self, project_name):
        if not self.connected:
            return 

        self.rpc.update(
            small_image="icon_python", small_text="Working on project", 
            large_image="main_icon", large_text="RedEngine", start=self.start_time,
            buttons=[{"label": "Visit Website", "url": "https://www.redegs.world/portfolio"}, {"label": "GitHub", "url": "https://github.com/RedEgs"}],
            details=f"Editing Project: {project_name}", state=f"Working In Project: {project_name}"
        ) # Set the presence
        self.project_name = project_name

    def engine_play_state(self):
        if not self.connected:
            return 

        if self.play_start == 0:
            self.play_start = time.time()
            
        self.rpc.update(
            small_image="play_icon_green", small_text="Running project", 
            large_image="main_icon", large_text="RedEngine", start=self.play_start,
            buttons=[{"label": "Visit Website", "url": "https://www.redegs.world/portfolio"}, {"label": "GitHub", "url": "https://github.com/RedEgs"}],
            details=f"Running Project: {self.project_name}", state=f"Working In Project: {self.project_name}"
        ) # Set the presence

    def engine_pause_state(self):
        if not self.connected:
            return 

        self.rpc.update(
            small_image="pause_icon", small_text="Paused project", 
            large_image="main_icon", large_text="RedEngine", start=time.time(),
            buttons=[{"label": "Visit Website", "url": "https://www.redegs.world/portfolio"}, {"label": "GitHub", "url": "https://github.com/RedEgs"}],
            details=f"Paused Project: {self.project_name}", state=f"Working In Project: {self.project_name}"
        ) # Set the presence
        
    def engine_default_state(self):
        if not self.connected:
            return 

        self.rpc.update(
            small_image="icon_python", small_text="Working on project", 
            large_image="main_icon", large_text="RedEngine", start=self.start_time,
            buttons=[{"label": "Visit Website", "url": "https://www.redegs.world/portfolio"}, {"label": "GitHub", "url": "https://github.com/RedEgs"}],
            details=f"Editing Project: {self.project_name}", state=f"Working In Project: {self.project_name}"
        ) # Set the presence
