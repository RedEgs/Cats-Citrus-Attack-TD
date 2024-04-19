import pytweening, pygame, sys, os, time, math

from engine.app import *
from engine.libs import SceneService as SceneService
from engine.libs import Maths
from engine.libs import CameraModule, GridModule, ParticleModule

# TODO FIX HIDING AND UNHIDING OF ELEMETNS

class Example_Scene(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        self.app = app
        self.camera = CameraModule.CameraComponent(app, pygame.Rect(0, 0, 1280, 720))
    
    
    
        # self.grid = GridModule.Grid(100, 50)
        # self.grid_surf = self.grid.pre_render_grid((2, 127, 252))
        self.sprite_stack = GuiService.SpriteStack(GuiService.GuiSpaces.WORLD, self.camera, (0,0), "spritestack.png", pygame.Rect(1, 8, 16, 16), scale_by=5, stack_spacing=1)
        #self.sprite_stack.hide()
        self.frame = 0
        

    def on_enter(self):
        super().on_enter()


    def update(self):
        self.frame += self.app.get_delta_time() * 15
        
        self.sprite_stack.set_angle(self.frame)
        #self.camera.track_target_raw(self.sprite_stack.rect)
        
        
        
        #print(self.sprite_stack.position, self.camera.get_camera_offset())
        # self.view_surf = self.camera.get_cropped_surface(pygame.Rect(600, 300, 100, 100))       


    def events(self, event):
        key = pygame.key.get_pressed()
        # if event.type == pygame.MOUSEBUTTONDOWN:
        if key[pygame.K_w]:
            self.camera.move_up(1)
            
        elif key[pygame.K_s]:
            self.camera.move_down(1)
            
        if key[pygame.K_a]:
            self.camera.move_left(1)
         
        elif key[pygame.K_d]:
            self.camera.move_right(1)
            
        # if key[pygame.K_e]:
        #     self.app.scene_service.switch_scene("example_scene_2")
            # if self.sprite_stack.visibility == True:
            #     self.sprite_stack.hide()
            # elif self.sprite_stack.visibility == False:
            #     self.sprite_stack.unhide()
                
                
                
            #self.camera.track_target_raw(self.sprite_stack.position)
            
            
            
            


    def draw(self, surface: pygame.Surface):
        surface.fill((2, 127, 252))
        # Draw horizontal line
        
        
        pygame.draw.line(surface, pygame.Color("red"), (0, 0-self.camera.get_camera_offset()[1]), (1280, 0-self.camera.get_camera_offset()[1]))

        # Draw vertical line
        pygame.draw.line(surface, pygame.Color("red"), (0-self.camera.get_camera_offset()[0], 0), (0-self.camera.get_camera_offset()[0], 720))     
        
        # surface.blit(self.grid_surf, (0-self.camera.get_camera_offset().x,
        #                               0-self.camera.get_camera_offset().y))

        pygame.draw.rect(surface, (255,255,255), pygame.Rect((self.sprite_stack.position), (100,  100)))
        # pygame.draw.rect(surface, "green", pygame.Rect(self.camera.get_camera_offset()-self.camera.get_camera_offset(), (30,  30)))
        # pygame.draw.rect(surface, (0, 0, 255), pygame.Rect((0, 0), (20,  20)))
        # pygame.draw.rect(surface, "yellow", pygame.Rect(self.camera.get_camera_center(), (10,  10)))
        
        # pygame.draw.rect(surface, (255, 255, 0), pygame.Rect((self.camera.get_camera_center()), (20,  20)))


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        