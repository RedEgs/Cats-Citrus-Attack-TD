import pytweening, pygame, sys, os, time, math


from engine.app import *
from engine.libs import SceneService as SceneService
from engine.libs import Maths
from engine.libs import CameraModule, GridModule, ParticleModule, SpecialEffectsModule
from engine.libs import TweenService


class Example_Scene(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        self.app = app
        self.camera = CameraModule.CameraComponent(app, pygame.Rect(0, 0, 1280, 720))
    


        self.last_update = pygame.time.get_ticks() 
        # self.grid = GridModule.Grid(100, 50)
        # self.grid_surf = self.grid.pre_render_grid((2, 127, 252))
        self.sprite_stack = GuiService.SpriteStack(GuiService.GuiSpaces.WORLD, self.camera, (100,0), "spritestack.png", pygame.Rect(1, 8, 16, 16), scale_by=5, stack_spacing=1)

    
        #self.sprite_stack.hide()
        self.frame = 0

        self.l_pos_1 = pygame.Vector2(-500, -500)
        self.l_pos_2 = pygame.Vector2(100, 100)
        
        self.tween = TweenService.Tween(self.l_pos_1, self.l_pos_2, 10, pytweening.easeInOutCubic, reverse=True, reverse_once=True)
        self.tween2 = TweenService.Tween(0, 255, 3, pytweening.easeInOutExpo)
        self.pressed = False

    def debug(self):
        print("debug")

    def on_enter(self):
        super().on_enter()


    def update(self):
        pass     
        # self.frame += self.app.get_delta_time() * 15
        
        # self.sprite_stack.set_angle(self.frame)
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
            
        if key[pygame.K_f]:
            if not self.pressed:
                self.app.scene_service.switch_scene("example_scene_2")
                self.pressed =True
                
        if key[pygame.K_g]:
            self.tween.start()
        
        if key[pygame.K_z]:
            self.tween2.start()
            
            
            
            
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
        
        
        pygame.draw.line(surface, pygame.Color("red"), pygame.Vector2(self.l_pos_1)-self.camera.get_camera_offset(), pygame.Vector2(self.l_pos_2)-self.camera.get_camera_offset())
        pygame.draw.rect(surface, (0, self.tween2.get_output(), 0), (self.tween.get_output()[0]-self.camera.get_camera_offset()[0], self.tween.get_output()[1]-self.camera.get_camera_offset()[1], 10, 10))



        #pygame.draw.line(surface, pygame.Color("red"), (0, 0-self.camera.get_camera_offset()[1]), (1280, 0-self.camera.get_camera_offset()[1]))

        # # Draw vertical line
        #pygame.draw.line(surface, pygame.Color("red"), (0-self.camera.get_camera_offset()[0], 0), (0-self.camera.get_camera_offset()[0], 720))     
        
        # # surface.blit(self.grid_surf, (0-self.camera.get_camera_offset().x,
        # #                               0-self.camera.get_camera_offset().y))

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        