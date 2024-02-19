import random, pygame, json, os, sys
from BlurWindow.blurWindow import blur

import win32api
import win32con
import win32gui


class Camera:
    def __init__(self, app, resolution, window_blur: False) -> None:
        self.app = app
        self.screen_w, self.screen_h = str(resolution).split("x")

        pygame.display.set_mode(
            (int(self.screen_w), int(self.screen_h)), depth=16, flags=pygame.DOUBLEBUF
        )  # Returns the actual screen
        self.screen = pygame.display.get_surface()

        self.display = pygame.Surface(
            (1280*2, 720*2)
        )  # Creates a virtual surface so a camera offset or zoom can be applied 
        self.camera_offset = pygame.math.Vector2(
            0, 0
        )  # The camera offset so the display can be moved left and right etc.
        self.camera_center = pygame.math.Vector2(
            self.display.get_size()[0] // 2, self.display.get_size()[1] // 2  # X  # Y
        ) # Gets center of screen for ease of access
        self.camera_zoom_scale = 1
        
        self.camera_bounds = {"left": 0, "right": 0, "top": 0, "bottom": 0}
        left = self.camera_bounds["left"]
        top = self.camera_bounds["top"]
        width = self.screen.get_size()[0] - (
            self.camera_bounds["left"] + self.camera_bounds["right"]
        )
        height = self.screen.get_size()[1] - (
            self.camera_bounds["top"] + self.camera_bounds["bottom"]
        )
        self.camera_bounds_rect = pygame.Rect(left, top, width, height)
        
        self.camera_event = pygame.USEREVENT
        self.camera_event_dragging = pygame.event.Event(self.camera_event, {"action": "dragging"})
        self.camera_event_up = pygame.event.Event(self.camera_event, {"action": "up"})
        self.camera_event_down = pygame.event.Event(
            self.camera_event, {"action": "down"}
        )
        self.camera_event_left = pygame.event.Event(
            self.camera_event, {"action": "left"}
        )
        self.camera_event_right = pygame.event.Event(
            self.camera_event, {"action": "right"}
        )
        self.camera_event_zoom_in = pygame.event.Event(
            self.camera_event, {"action": "zoom_in"}
        )
        self.camera_event_zoom_out = pygame.event.Event(
            self.camera_event, {"action": "zoom_out"}
        )

        self.camera_moving = False   


        # Dont mind this, just a little experiment
        if window_blur:
            hwnd = pygame.display.get_wm_info()["window"]
            blur(hwnd, Dark=True)
            win32gui.SetWindowLong(
                hwnd,
                win32con.GWL_EXSTYLE,
                win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                | win32con.WS_EX_LAYERED,
            )
            win32gui.SetLayeredWindowAttributes(
                hwnd, win32api.RGB(*(235, 235, 235)), 0, win32con.LWA_COLORKEY
            )

    def events(self, event):
        if event.type == pygame.MOUSEWHEEL:
            prev_scale = self.camera_zoom_scale
            
            if self.camera_zoom_scale >= 0.51:
                self.camera_zoom_scale += event.y * 0.01
            else:
                self.camera_zoom_scale = 0.51
                
            if self.camera_zoom_scale <= 1.75:
                self.camera_zoom_scale += event.y * 0.01
            else:
                self.camera_zoom_scale = 1.75
            
            
            new_scale = self.camera_zoom_scale 
        
            if new_scale > prev_scale:
                pygame.event.post(self.camera_event_zoom_in)
            else:
                pygame.event.post(self.camera_event_zoom_out)
                
        
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 2:
        #         self.camera_moving = True
                
        # if event.type == pygame.MOUSEBUTTONUP:
        #     if event.button == 2:
        #         self.camera_moving = False        
            
        # if self.camera_moving == True:  
        #     if event.type == pygame.MOUSEMOTION:
        #         self.camera_offset = pygame.math.Vector2(event.rel[0], event.rel[1])
                
        #         pygame.event.post(self.camera_event_dragging)
                
            #self.camera_bounds_rect.camera_offset = event.rel
        
        
        
        if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_LSHIFT:
        #         if self.camera_zoom_scale < 2:
        #             self.camera_zoom_scale += 0.01
        #             pygame.event.post(self.camera_event_zoom_in)

        #     if event.key == pygame.K_LCTRL:
        #         if self.camera_zoom_scale > 0.5:
        #             self.camera_zoom_scale -= 0.01
        #             pygame.event.post(self.camera_event_zoom_out)
                    
            if event.key == pygame.K_UP:
                self.camera_offset[1] -= 1
            
                pygame.event.post(self.camera_event_up)

            if event.key == pygame.K_DOWN:
                self.camera_offset[1] += 1
                
                
                
                pygame.event.post(self.camera_event_down)

            if event.key == pygame.K_LEFT:
                self.camera_offset[0] -= 1
                
                
                
                pygame.event.post(self.camera_event_left)

            if event.key == pygame.K_RIGHT:
                self.camera_offset[0] += 1
                
                pygame.event.post(self.camera_event_right)
 

    def update(self):
        pass

    def draw(self):
        pygame.draw.circle(self.display, (0, 180, 255), (self.camera_bounds_rect.center[0] / self.camera_zoom_scale, 
                                                         self.camera_bounds_rect.center[1]  / self.camera_zoom_scale), 
                                                         5/self.camera_zoom_scale)
        
        self.screen.blit(
            pygame.transform.scale( # Scales the display so it can be zoomed or resized.
                self.display,
                (
                    self.display.get_size()[0] * self.camera_zoom_scale,
                    self.display.get_size()[1] * self.camera_zoom_scale,
                ),
            ),  
            (0,0), # Display offset, Normally camera_offset would go here
            area=self.camera_bounds_rect, # The area that is rendered, the camera bounds
        )
        
        # Draws global or screen space elements under here
        
        for element in self.app.guis.screen_ui_elements:
            element.draw(self.screen)
            element.update()
            element.update_position()
    
        for element in self.app.guis.global_ui_elements:
            element.draw(self.screen)
            element.update()
            element.update_position()
        
        
    

        pygame.draw.rect(self.screen, (0, 180, 255), self.camera_bounds_rect, 5) # Draws the rect in which everything is visible within the camera
        pygame.draw.circle(self.screen, (255, 180, 0), self.camera_bounds_rect.topleft, 5)
        pygame.display.update(self.camera_bounds_rect) # Visually updates only what the window/camera can see

    def focus_target(self, target: pygame.rect):
        self.camera_offset = target.center - self.camera_center

    def check_camera_bounds(self, target: pygame.Rect):
        return self.camera_bounds_rect.colliderect(target)



    def get_display(self):
        return self.display

    def get_screen(self):
        return self.screen

    def get_display_output_size(self):
        scaled_res = (round(self.display.get_size()[0] * self.camera_zoom_scale, 2), round(self.display.get_size()[1] * self.camera_zoom_scale, 2))
        return scaled_res

    def get_zoom(self):
        return self.camera_zoom_scale

    def get_camera_offset(self):
        return self.camera_offset

    def get_camera_center(self):
        return self.camera_center
