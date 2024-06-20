import pytweening, pygame, sys, os, time, math

import pyredengine as pyr
from  pyredengine import SceneService as SceneService
from  pyredengine import CameraModule, GridModule, ParticleModule, SpecialEffectsModule
from  pyredengine import TweenService
from  pyredengine import GuiService
# h1
class Example_Scene(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        self.app = app
        self.camera = CameraModule.CameraComponent(app, pygame.Rect(0, 0, 1280, 720))
        
        self.cont_time = 0.0


    def on_enter(self):
        super().on_enter()


        

    def update(self):
        self.cont_time += 0.01

 


    def events(self, event):#
        print(event)
        # if event.type == pygame.KEYDOWN:
        #     print("key press recieved")
        #     if event.key == pygame.K_w:
        #         self.camera.move_up(1)
        #     elif event.key == pygame.K_s:
        #         self.camera.move_down(1)
        #     elif event.key == pygame.K_a:
        #         self.camera.move_left(1)
        #     elif event.key == pygame.K_d:
        #         self.camera.move_right(1)
        #     elif event.key == pygame.K_f:
        #         if not self.pressed:
        #             self.app.scene_service.switch_scene("example_scene_2")
        #             self.pressed = True
        #     elif event.key == pygame.K_g:
        #         self.tween.start()
        #     elif event.key == pygame.K_z:
        #         self.tween2.start()
            

            


    def draw(self, surface: pygame.Surface):
        surface.fill((0, 0, 255))
  
        
        
        import math
        
        
        pygame.draw.circle(surface, (0, 0, 0), (1280//2 + math.sin(self.cont_time) * 100, 
                                                       720//2), 20)
        
        
        
        
        
        
        
        
        