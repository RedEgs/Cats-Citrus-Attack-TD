import pyglet
from pyglet import window

import numpy as np

import libs.GuiLib as GuiLib


class Window(window.Window):
    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        
        icon16 = pyglet.image.load('icon16.png')
        icon32 = pyglet.image.load('icon32.png')
        self.set_icon(icon16, icon32)
        
        
        if self._style == self.WINDOW_STYLE_BORDERLESS:
            
            self.gui_frame = pyglet.gui.Frame(self, order=1)
            self.window_header = GuiLib.WindowHeader(window=self) 
            self.gui_frame.add_widget(self.window_header)
        pyglet.gl.glClearColor(.13,.13,.13,1) # Note that these are values 0.0 - 1.0 and not (0-255).




        # self.display_center = np.array([self.display.get_default_screen().width/4, self.display.get_default_screen().height/4]) # Get Center of the current monitor
        # self.set_location(int(self.display_center[0]), int(self.display_center[1])) # Set it to the center

        
    def run(self): 
        """
        Ran once by the engine app, this function is explicit
        """
        pyglet.app.run() 

    def on_draw(self):
        """
        Called when window is drawn, this function is explicit
        """
        self.clear()
        
        if self._style == self.WINDOW_STYLE_BORDERLESS:
            self.window_header.draw()
