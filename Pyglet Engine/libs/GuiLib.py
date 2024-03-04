import pyglet
from pyglet import window
from pyglet import gui
from pyglet import shapes


from pyglet.image import Framebuffer
from pyglet.image.codecs.png import PNGImageDecoder
from functools import cache
from enum import Enum

import pyautogui, numba
import numpy as np
from pyglet.window.cocoa import CocoaWindow as Window
from pyglet.window.headless import HeadlessWindow as Window
from pyglet.window.win32 import Win32Window as Window
from pyglet.window.xlib import XlibWindow as Window


class ExtendedWidget(gui.WidgetBase):
    def __init__(self, x, y, width, height, window: window.Window = None, batch: pyglet.graphics.Batch = None):
        super().__init__(x, y, width, height)
        self._window = window

        if batch == None:
            self._widget_batch = pyglet.graphics.Batch()
        else:
            self._widget_batch = batch

        
    def _check_area(self, x, y, area_x, area_y, area_width, area_height):
        return area_x <= x <= area_x + area_width and area_y <= y <= area_y + area_height
    
    def get_mouse_screen_position(self):
        pos = pyautogui.position()
        return pos[0], pos[1]

    def draw(self):
        self._widget_batch.draw()
   
   
    
class WindowHeader(ExtendedWidget): 
    def __init__(self, x=0, y=760-30, width=1280, height=30, window: pyglet.window.Window = None):
        super().__init__(x, y, width, height, window)
        self.window_batch = pyglet.graphics.Batch()
        
     
        
        self.header_size = 30
        self.header_rect = shapes.Rectangle(x, y, width, height, batch=self.window_batch)
    
        self.button_size = 16
    
        self.close_button_rect = shapes.Rectangle(self._top_right[0]-self.header_size, 
                                                  self._top_right[1], 
                                                  self.header_size, self.header_size, 
                                                  color=(255,0,0),
                                                  batch=self.window_batch)
    
        self.maximise_button_rect = shapes.Rectangle(self._top_right[0]-self.header_size*2, 
                                                    self._top_right[1], 
                                                    self.header_size, self.header_size, 
                                                    color=(0,255,0),
                                                    batch=self.window_batch)
        
        self.minimise_button_rect = shapes.Rectangle(self._top_right[0]-self.header_size*3, 
                                                    self._top_right[1], 
                                                    self.header_size, self.header_size, 
                                                    color=(0,0,255),
                                                    batch=self.window_batch)
    
    
    
    
        # close_icon = pyglet.image.load("close.png", decoder=PNGImageDecoder())
        # close_button_x = x+(1280-self.header_size)
        # self.close_sprite = pyglet.sprite.Sprite(close_icon, close_button_x, 760-(height//2))
        
    
    
    
        self.dragging_window = False
        self.dragged_position_start = np.array([0,0])
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        super().on_mouse_press(x, y, buttons, modifiers)
        clicked_position = np.array([x,y])

        c_rect = self.close_button_rect
        ma_rect = self.maximise_button_rect
        mi_rect = self.minimise_button_rect

        if self._check_area(x, y, c_rect._x, c_rect._y, c_rect._width, c_rect._height): # Close
            self._window.close() 
            
        elif self._check_area(x, y, ma_rect._x, ma_rect._y, ma_rect._width, ma_rect._height): # Maximise
            print("feature is yet to implemented")
            # self._window.maximize()
            # self.reload_header()
              
        elif self._check_area(x, y, mi_rect._x, mi_rect._y, mi_rect._width, mi_rect._height): # Minimise
            print("feature is yet to implemented")
            # self._window.minimize()    
        
        
        
        else: # Drag Window
            self.dragged_position_start = clicked_position
            self.dragging_window = True
            
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        super().on_mouse_drag(x, y, dx, dy, buttons, modifiers)
          
        
        if self.dragging_window:
            o_x, o_y = self.dragged_position_start.tolist()
            m_x, m_y = self.get_mouse_screen_position()    
        
            self._window.set_location(m_x-o_x, (o_y+m_y)-760)
            
            self.dispatch_event("on_window_move")
        
    def on_mouse_release(self, x, y, buttons, modifiers):
        super().on_mouse_release(x, y, buttons, modifiers)
        
        self.dragging_window = False  
    
    def draw(self):
        self.window_batch.draw()
        
        
        # self.close_sprite.draw()
WindowHeader.register_event_type("on_window_move")



class Panel(ExtendedWidget):
    # top of the panel = (self._y+self._height)
    
    
    
    def __init__(self, x, y, width, height, window: window.Window = None, widget_title: str = "Panel"):
        super().__init__(x, y, width, height, window)
        
        self._widget_title = widget_title
        self.panel_rect = self._load_panel()
    
    def _load_panel(self):
        panel_rect = shapes.BorderedRectangle(self._x, self._y, self._width, self._height, 2, (18,18,18), (38,38,38), self._widget_batch)
        # panel_rect.anchor_x = self.x+self.width//2
        # panel_rect.anchor_y = self.x+self.height//2
        
        return panel_rect
        
        
class PanelWidget(ExtendedWidget):
    # top of the panel = (self._y+self._height)
    
    
    
    def __init__(self, x, y, width, height, window: window.Window = None, widget_title: str = "Panel"):
        super().__init__(x, y, width, height, window)
        
        self._widget_title = widget_title

        #self.drop_shadow = self.render_drop_shadow()
        self.panel_rect = self._load_panel()
        self.title_pane_rect = self._load_title_panel()
        #self._widget_title = self._load_title()


        
    
    
    def _load_panel(self):
        panel_rect = shapes.BorderedRectangle(self._x, self._y, self._width, self._height, 2, (18,18,18), (38,38,38), self._widget_batch)
        panel_rect.anchor_x = self.width//2
        panel_rect.anchor_y = self.height//2
        
        return panel_rect
     
    def _load_title_panel(self):
        title_panel_rect = shapes.BorderedRectangle(self._x, (self._y+self._height), self._width, 22, 2, (23,23,23), (38,38,38), self._widget_batch)
        title_panel_rect.anchor_x = self.width//2
        title_panel_rect.anchor_y = self.height//2    
    
        return title_panel_rect
    
    def _load_title(self):
        widget_title = pyglet.text.Label(self._widget_title,
                          font_name='Segoe UI',
                          font_size=10,
                          x=(self.title_pane_rect.width//4)-(18), y=self.title_pane_rect._y+(12),
                          batch=self._widget_batch)
    
        widget_title.anchor_x = self.width//2
        widget_title.anchor_y = self.height//2
        
        return widget_title
    
    
    
    # def render_drop_shadow(self):
    #     new_panel = shapes.Rectangle(self.x, self.y, self.width*1.2, self.height*1.2, (255,0,0), self._widget_batch)

    
    #     return new_panel
 
 
class GridWidget(ExtendedWidget):
    def __init__(self, x, y, width, height, window: window.Window = None, batch: shapes.Batch = None):
        super().__init__(x, y, width, height, window, batch)
        self.buffer_texture = pyglet.image.Texture.create(1280, 720)
        self.framebuffer = Framebuffer()
        self.framebuffer.attach_texture(self.buffer_texture)

    

    
    
    
           
class ShaderWidget(ExtendedWidget):
    def __init__(self, x, y, width, height, window: window.Window = None, batch: shapes.Batch = None):
        super().__init__(x, y, width, height, window, batch)
        self.buffer_texture = pyglet.image.Texture.create(300, 300)
        self.framebuffer = Framebuffer()
        self.framebuffer.attach_texture(self.buffer_texture)
        
        self.rectangle = pyglet.shapes.Rectangle(10, 20, 100, 200)
        
        self.vertex_source = """#version 150 core
        in vec3 translate;
        in vec4 colors;
        in vec3 tex_coords;
        in vec2 scale;
        in vec3 position;
        in float rotation;

        out vec4 vertex_colors;
        out vec3 texture_coords;

        uniform WindowBlock
        {
            mat4 projection;
            mat4 view;
        } window;

        mat4 m_scale = mat4(1.0);
        mat4 m_rotation = mat4(1.0);
        mat4 m_translate = mat4(1.0);

        void main()
        {
            m_scale[0][0] = scale.x;
            m_scale[1][1] = scale.y;
            m_translate[3][0] = translate.x;
            m_translate[3][1] = translate.y;
            m_translate[3][2] = translate.z;
            m_rotation[0][0] =  cos(-radians(rotation));
            m_rotation[0][1] =  sin(-radians(rotation));
            m_rotation[1][0] = -sin(-radians(rotation));
            m_rotation[1][1] =  cos(-radians(rotation));

            gl_Position = window.projection * window.view * m_translate * m_rotation * m_scale * vec4(position, 1.0);

            vertex_colors = colors;
            texture_coords = tex_coords;
        }
    """

        self.fragment_source = """#version 150 core
        in vec4 vertex_colors;
        in vec3 texture_coords;
        out vec4 final_colors;

        uniform sampler2D sprite_texture;
        uniform float time;

        void main()
        {
            // Apply a static sin wave effect
            vec2 coord = texture_coords.xy + sin(10. * texture_coords.y) * time;
            coord = clamp(coord, 0., 1.);

            final_colors = texture(sprite_texture, coord) * vertex_colors;
        }
    """
    
        self.wave_shader_program = pyglet.gl.current_context.create_program(
        (self.vertex_source, 'vertex'), (self.fragment_source, 'fragment'))

        # Create a sprite encapsulating the buffer texture, setting the new shader
        # for rendering.
        self.buffer_sprite = pyglet.sprite.AdvancedSprite(self.buffer_texture,
                                                    program=self.wave_shader_program)

    def draw(self):
        self.framebuffer.bind()
        self._window.clear()
        self.rectangle.draw()
        self.framebuffer.unbind()
        self._window.clear()
        self.buffer_sprite.draw()