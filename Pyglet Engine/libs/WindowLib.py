import pyglet
from pyglet import window

import numpy as np
from enum import Enum
import libs.GuiLib as GuiLib

# class window_positions(Enum):
#     TOP_LEFT = np.array([0, self.height]).any(),
#     TOP_MIDDLE = np.array([self.width//2, self.height]).any(),
#     TOP_RIGHT = np.array([self.width, self.height]).any(),
    
#     MIDDLE_LEFT = np.array([0, self.height//2]).any()
#     CENTER = np.array([self.width//2, self.height//2]).any(),
#     MIDDLE_RIGHT = np.array([self.width, self.height//2]).any(),
    
#     BOTTOM_LEFT = np.array([0, 0]).any(),
#     BOTTOM_MIDDLE = np.array([self.width//2, 0]).any(),
#     BOTTOM_RIGHT = np.array([self.width, 0]).any(),
            

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
        
        self.gui_frame = pyglet.gui.Frame(self, order=1)
        self.panel = GuiLib.Panel(0, 0, 200, 10, self)
        
        self.shader_test = GuiLib.ShaderWidget(100, 100, 100, 100, self)
        
        #self.panel1 = GuiLib.PanelWidget(0+100, self.height//2-100, 200, 400, self)


        pyglet.gl.glClearColor(.1,.1,.1,1) # Note that these are values 0.0 - 1.0 and not (0-255).

        
        
        
        
        
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
        self.panel.draw()
        self.shader_test.draw()