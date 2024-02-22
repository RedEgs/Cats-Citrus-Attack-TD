import pyglet
from libs.WindowLib import Window

class App:
    def __init__(self):
        self.main_window = Window(1280, 720+40, "PyRedEngine", resizable=False)
        # hello
        
        
        
        
    def run(self):
        self.main_window.run()
        
        
        
app = App()        
app.run()  
