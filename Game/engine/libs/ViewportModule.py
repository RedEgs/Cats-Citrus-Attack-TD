import random, pygame, moderngl, json, os, sys

from array import array
from engine.libs.Services import Service
from engine.libs import CameraModule


class Viewport(Service):
    def __init__(self, app) -> None:
        self.app = app
        
        self.load_settings_from_config()
        
        if self.workspace_settings["use-opengl"]:
            self.load_screen_opengl()
            self.load_shaders()
            
        else: self.load_screen_default()
        
        self.load_viewport()
        self.load_viewport_settings()
        
        
        if self.experimental_features["enable-window-blurring"]:
            blur_color = self.experimental_features["color-to-blur"]#print()
            self.load_window_blur(blur_color)
               
       
    def load_settings_from_config(self):
        if not self.app._override_config:
        
            with open("config.json", "r") as conf:
                data_raw = json.load(conf)
                
                self.app_settings = data_raw["app"]["settings"]
                self.workspace_settings = data_raw["workspace"]["settings"]
                self.camera_settings = data_raw["camera"]["settings"]
                self.experimental_features = data_raw["experimental"]["features"]

            # Load resolution from file
            resolution = self.app_settings["resolution"]
            self.screen_w, self.screen_h = str(resolution).split("x")

        else:
            data_raw = json.loads(self.app._override_config_text)
            
            self.app_settings = data_raw["app"]["settings"]
            self.workspace_settings = data_raw["workspace"]["settings"]
            self.camera_settings = data_raw["camera"]["settings"]
            self.experimental_features = data_raw["experimental"]["features"]
            
            resolution = self.app_settings["resolution"]
            self.screen_w, self.screen_h = str(resolution).split("x")

        
    
    def load_screen_default(self):
        """
        Loads the display for the pygame window, with resolution from config
        """   
        # Initialise and create the actual display
        if not self.app._qt_mode:
            pygame.display.set_mode(
                (int(self.screen_w), int(self.screen_h)), depth=16, flags=pygame.DOUBLEBUF
            ) 
            self.screen = pygame.display.get_surface()
        else:
            self.app._hwnd = None
            if len(sys.argv) > 1:
                self.app._hwnd = int(sys.argv[1])
                os.environ['SDL_WINDOWID'] = str(self.app._hwnd)
            
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (-1000, -1000)
        
            pygame.display.set_mode(
                (int(self.screen_w), int(self.screen_h)), depth=16, flags=pygame.NOFRAME
            ) 
            self.screen = pygame.display.get_surface()
            
    
    def load_screen_opengl(self):
        """
        Loads the display for the pygame window, with resolution from config
        """   
        # Initialise and create the actual display
        pygame.display.set_mode(
            (int(self.screen_w), int(self.screen_h)), depth=16, flags=pygame.OPENGL | pygame.DOUBLEBUF 
        ) 
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_ACCELERATED_VISUAL, 1)
        
        
        self.screen = pygame.display.get_surface()
        self._ctx = moderngl.create_context()
        
        self._quad_buffer = self.get_gl_screen_bounds(self.screen.get_rect(), self._ctx)
        
        # self._quad_buffer = self._ctx.buffer(data=array('f', [
        #     # position (x, y), uv coords (x, y)
        #     -1.0, 1.0, 0.0, 0.0,  # topleft
        #     1.0, 1.0, 1.0, 0.0,   # topright
        #     -1.0, -1.0, 0.0, 1.0, # bottomleft
        #     1.0, -1.0, 1.0, 1.0,  # bottomright
        # ]))
      
    def load_shaders(self):
        self._vert_shader = '''
        #version 330 core

        in vec2 vert;
        in vec2 texcoord;
        out vec2 uvs;

        uniform float time = 0;

        void main() {
            uvs = texcoord;
            gl_Position = vec4(vert, 0.0, 1.0);

        }
        '''
        
        self._frag_shader = '''
        #version 330 core
        uniform sampler2D tex;

        in vec2 uvs;
        out vec4 f_color;

        void main()
        {
            f_color = texture(tex, uvs);
        }
        '''
        
        self._program = self._ctx.program(vertex_shader=self._vert_shader, fragment_shader=self._frag_shader)
        self._render_object = self._ctx.vertex_array(self._program, [(self._quad_buffer, '2f 2f', 'vert', 'texcoord')])
                            
    def load_viewport(self, camera: any = None):   
        """
        Will take in a camera, if none is given, it will assume a defualt camera locked at (0,0)
        Camera type is taken the `CameraModule.py` every scene should have a camera even those consisting of only GUI
        With the exception of the TransitionService
        """
    
        self.main_camera = CameraModule.CameraComponent(self.app, pygame.Rect(0,0 , int(self.screen_w), int(self.screen_h)))
        
        self.camera_offset = self.main_camera.get_camera_offset()
        self.camera_bounds = self.main_camera.get_camera_bounds()
        self.camera_bounds_rect = self.main_camera.get_camera_bounds()
        
        if self.workspace_settings["use-opengl"]: self.draw_screen = self.draw_display_opengl
        else: self.draw_screen = self.draw_display_default
        
    def load_viewport_settings(self):
        self.camera_zoom_scale = 1
    
        self.load_camera_event()
    
    def load_window_blur(self, blur_color): # Not important, just a small "easter egg"
        from BlurWindow.blurWindow import blur
        import win32api, win32con, win32gui
        
        hwnd = pygame.display.get_wm_info()["window"]
        blur(hwnd, Dark=True)
        win32gui.SetWindowLong(
            hwnd,
            win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            | win32con.WS_EX_LAYERED,
        )
        win32gui.SetLayeredWindowAttributes(
            hwnd, win32api.RGB(*(blur_color)), 0, win32con.LWA_COLORKEY
        )


    def load_camera_event(self):
        self.app.camera_event = pygame.USEREVENT
        self.app.camera_event_dragging = pygame.event.Event(self.app.camera_event, {"action": "dragging"})
        self.app.camera_event_up = pygame.event.Event(self.app.camera_event, {"action": "up"})
        self.app.camera_event_down = pygame.event.Event(
            self.app.camera_event, {"action": "down"}
            )
        self.app.camera_event_left = pygame.event.Event(
            self.app.camera_event, {"action": "left"}
            )
        self.app.camera_event_right = pygame.event.Event(
            self.app.camera_event, {"action": "right"}
            )
        self.app.camera_event_zoom_in = pygame.event.Event(
            self.app.camera_event, {"action": "zoom_in"}
            )
        self.app.camera_event_zoom_out = pygame.event.Event(
            self.app.camera_event, {"action": "zoom_out"}
            )
        self.app.camera_event_shake = pygame.event.Event(
            self.app.camera_event, {"action": "shake"}
            )

    def draw_display_opengl(self):
        self.tex = self.to_texture(self.get_main_camera_surface())
        self._frame_tex = self.tex
        self._frame_tex.use(0)
        self._program['tex'] = 0
        self._render_object.render(mode=moderngl.TRIANGLE_STRIP)
        
        pygame.display.flip()
        #self.screen.blit(self.get_main_camera_surface(), (0,0), area=self.get_camera_bounds())
            
    def draw_display_default(self):
        self.screen.blit(self.get_main_camera_surface(), (0,0), area=self.get_camera_bounds())
        pygame.display.update(self.get_camera_bounds())
                    
    def draw(self): 
        self.app.transition_service.draw(self.get_main_camera_surface())
        self.draw_screen()
        if self.workspace_settings["use-opengl"]: self._frame_tex.release()

        
        #pygame.display.update(self.main_camera.get_camera_bounds()) # Visually updates only what the window/camera can see


    def get_gl_screen_bounds(self, rect, ctx, top_offset = 0, bottom_offset = 0, return_rect = None, return_list = None, rotate = 0, x_mul = 1):
        win_w, win_h = int(self.screen_w), int(self.screen_h)
        l, t, r, b = rect
        r_w_w = 1 / win_w
        r_w_h = 1 / win_h
        no_t = (t * r_w_h) * -2 + 1
        no_b = ((t + b) * r_w_h) * -2 + 1
        no_l = (l * r_w_w) * 2 - 1
        no_r = ((r + l) * r_w_w) * 2 - 1 

        buffer = [
                # position (x, y), uv coords (x, y)
                no_l + top_offset, no_t, 0, 0,  # topleft
                no_r + top_offset, no_t, 1, 0,  # topright
                no_l + bottom_offset, no_b, 0, 1,  # bottomleft
                no_r + bottom_offset, no_b, 1, 1,  # bottomright
            ]

        if not return_rect:
            quad_buffer = ctx.buffer(data=array('f', buffer))

        return (quad_buffer if not return_list else buffer) if not return_rect else (no_l, no_t, no_r, no_b)

    def to_texture(self, surf):
        self.tex = self._ctx.texture(surf.get_size(), 4)
        self.tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.tex.swizzle = 'BGRA'
        self.tex.write(surf.get_view('1'))
        return self.tex
        
    def set_main_camera(self, camera: CameraModule.CameraComponent):
        self.main_camera = camera
    
    def get_main_camera(self):
        return self.main_camera 

    def get_main_camera_surface(self):
        return self.main_camera.get_camera_surface()

    def get_screen(self):
        return self.screen

    def get_display_output_size(self):
        return round(
            self.get_main_camera_surface().get_size()[0] * self.camera_zoom_scale, 2
        ), round(self.get_main_camera_surface().get_size()[1] * self.camera_zoom_scale, 2)

    def get_zoom(self):
        return self.camera_zoom_scale

    def get_camera_offset(self):
        return self.main_camera.get_camera_offset()

    def get_camera_center(self):
        return self.main_camera.get_camera_center()

    def get_camera_bounds(self):
        return self.main_camera.get_camera_bounds()
    
    
    
    
    
    
    
    
    
