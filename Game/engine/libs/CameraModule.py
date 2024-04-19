from engine.libs.Services import Service
from pygame import gfxdraw
import random, pygame, json, os, sys


class CameraComponent():
    def __init__(self, app, camera_bounds: pygame.Rect):
        """
        X, Y - Position of camera in the world 
        W, H - Size of camera (The output resolution/viewport)
        
        """
        self.app = app
        self.camera_bounds = camera_bounds
        self.load_camera()
        
    
    def load_camera(self):
        self.camera_surface = pygame.Surface((self.camera_bounds.width, self.camera_bounds.height))

        self.camera_offset = pygame.math.Vector2(self.camera_bounds.x-int(self.camera_surface.get_rect().w)/2, 
                                                 self.camera_bounds.y-int(self.camera_surface.get_rect().h)/2) 
        
        
        self.camera_center = pygame.Vector2(int(self.camera_surface.get_rect().w)//2, int(self.camera_surface.get_rect().h)//2)
        # Centers the camera to be 0,0

        #self.camera_surface.set_clip(self.camera_bounds)
        self.bounds = {"left": 0, "right": 0, "top": 0, "bottom": 0}
        left = self.bounds["left"]
        top = self.bounds["top"]
        width = self.camera_surface.get_size()[0] - (
            self.bounds["left"] + self.bounds["right"]
        )
        height = self.camera_surface.get_size()[1] - (
            self.bounds["top"] + self.bounds["bottom"]
        )
        self.camera_bounds_rect = pygame.Rect(left, top, width, height)
        # self.camera_bounds_rect = self.camera_surface.get_rect()

    def move_up(self, amount: int):
        self.camera_offset.y -= amount
        pygame.event.post(self.app.camera_event_up)

    def move_down(self, amount: int):
        self.camera_offset.y += amount
        pygame.event.post(self.app.camera_event_down)

    def move_left(self, amount: int):
        self.camera_offset.x -= amount
        pygame.event.post(self.app.camera_event_left)

    def move_right(self, amount: int):
        self.camera_offset.x += amount
        pygame.event.post(self.app.camera_event_right)

    def track_target_raw(self, target: pygame.Rect):
        self.camera_offset[0] = target.centerx - self.camera_center[0]
        self.camera_offset[1] = target.centery - self.camera_center[1]
        
    
    def shake_camera(self, shake_amount: int):
        self.camera_offset[0] += random.randint(0, shake_amount) - (shake_amount//2)
        self.camera_offset[1] += random.randint(0, shake_amount) - (shake_amount//2)

        for _ in range(shake_amount):
            pygame.event.post(self.app.camera_event_shake)

    def update_camera(self):
        pass
        # offsetX = cameraRect.x + cameraRect.w/2 - (entity.camera.worldX * entity.camera.zoomLevel)
        # offsetY = cameraRect.y + cameraRect.h/2 - (entity.camera.worldY * entity.camera.zoomLevel)

    def check_camera_bounds_rect(self, target: pygame.Rect):
        return self.camera_bounds_rect.colliderect(target)

    def check_camera_bounds_position(self, target: pygame.Vector2):
        return (
            target.x < -50
            or target.x > self.camera_bounds.w + 50
            or target.y < -50
            or target.y > self.camera_bounds.h + 50
        )

    def get_camera_resolution(self):
        return pygame.Vector2(int(self.camera_bounds.w), int(self.camera_bounds.h))
        
    def get_cropped_surface(self, cropping_rect: pygame.Rect):
        return self.camera_surface.subsurface(cropping_rect).copy()

    def get_clipping_rect(self):
        return self.clipping_rect
    
    def get_camera_bounds(self):
        return self.camera_bounds_rect
    
    def get_camera_center(self):
        return self.camera_center
    
    def get_camera_offset(self):
        return self.camera_offset
    
    def get_camera_position(self):
        return self.camera_position
    
    def get_camera_surface(self):
        return self.camera_surface
    
    
