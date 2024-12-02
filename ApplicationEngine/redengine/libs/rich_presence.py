from pypresence import Presence
from functools import wraps
import time, threading

def run_methods_in_thread(cls):
    """A class decorator to make all methods run in a thread."""
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if callable(attr) and not attr_name.startswith("__"):
            # Wrap the method with threading logic
            @wraps(attr)
            def wrapper(self, *args, **kwargs):
                thread = threading.Thread(target=attr, args=(self, *args), kwargs=kwargs, daemon=True)
                thread.start()
                return thread
            setattr(cls, attr_name, wrapper)
    return cls

#@run_methods_in_thread
class RichPresenceHandler():
    def __init__(self):
        self.client_id = "1312502880233853079"
        self.rpc = Presence(self.client_id)  # Initialize the client class
        self.rpc.connect() # Start the handshake loop
        
        self.start_time = time.time()
        self.play_start = 0

    def launcher_state(self):
        self.rpc.update(
            small_image="launcher_icon_background", small_text="Inside the launcher", 
            large_image="main_icon", large_text="RedEngine", start=self.start_time,
            buttons=[{"label": "Visit Website", "url": "https://www.redegs.world/portfolio"}, {"label": "GitHub", "url": "https://github.com/RedEgs"}],
            details="Inside of the launcher", state="In The Launcher"
        ) # Set the presence

    def engine_state(self, project_name):
        self.rpc.update(
            small_image="icon_python", small_text="Working on project", 
            large_image="main_icon", large_text="RedEngine", start=self.start_time,
            buttons=[{"label": "Visit Website", "url": "https://www.redegs.world/portfolio"}, {"label": "GitHub", "url": "https://github.com/RedEgs"}],
            details=f"Editing Project: {project_name}", state=f"Working In Project: {project_name}"
        ) # Set the presence
        self.project_name = project_name

    def engine_play_state(self):
        if self.play_start == 0:
            self.play_start = time.time()
            
        self.rpc.update(
            small_image="play_icon_green", small_text="Running project", 
            large_image="main_icon", large_text="RedEngine", start=self.play_start,
            buttons=[{"label": "Visit Website", "url": "https://www.redegs.world/portfolio"}, {"label": "GitHub", "url": "https://github.com/RedEgs"}],
            details=f"Running Project: {self.project_name}", state=f"Working In Project: {self.project_name}"
        ) # Set the presence

    def engine_pause_state(self):
        self.rpc.update(
            small_image="pause_icon", small_text="Paused project", 
            large_image="main_icon", large_text="RedEngine", start=time.time(),
            buttons=[{"label": "Visit Website", "url": "https://www.redegs.world/portfolio"}, {"label": "GitHub", "url": "https://github.com/RedEgs"}],
            details=f"Paused Project: {self.project_name}", state=f"Working In Project: {self.project_name}"
        ) # Set the presence
        
    def engine_default_state(self):
        self.rpc.update(
            small_image="icon_python", small_text="Working on project", 
            large_image="main_icon", large_text="RedEngine", start=self.start_time,
            buttons=[{"label": "Visit Website", "url": "https://www.redegs.world/portfolio"}, {"label": "GitHub", "url": "https://github.com/RedEgs"}],
            details=f"Editing Project: {self.project_name}", state=f"Working In Project: {self.project_name}"
        ) # Set the presence