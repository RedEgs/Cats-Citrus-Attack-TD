import pytweening, pygame, sys, os, time, math

from engine.app import *
from engine.libs import SceneService as SceneService
from engine.libs import Maths
from engine.libs import CameraModule

class Example_Scene(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        self.app = app
        self.camera = CameraModule.CameraComponent(self.app, pygame.Rect(0,0, 1280, 720))
        
        # All Normal GUI Elements

        # GuiService.TextElement(
        #     GuiService.GuiSpaces.SCREEN,
        #     self.camera,
        #     (800, 100),
        #     "tETS tETX blox",
        #     24,
        #     (0, 0, 0),
        #     "left",
        # )
        #self.img = GuiService.ImageElement(GuiService.GuiSpaces.WORLD, self.camera, (0,0),"test_image.png")
        
        # GuiService.StatusBar(GuiService.GuiSpaces.SCREEN, self.camera, (100, 400), (100, 50), initial_value=10)
        
        # GuiService.EasyCurve(GuiService.GuiSpaces.SCREEN, self.camera, (100,100), (200, 200))
        
        
        # All Event Elements
        # GuiService.TextInput(GuiService.GuiSpaces.SCREEN, self.camera, (700, 200), 24, "test input")
        # GuiService.Slider(GuiService.GuiSpaces.SCREEN, self.camera, (200, 300), (100, 25))
        # GuiService.Checkbox(GuiService.GuiSpaces.SCREEN, self.camera, (100, 300))
        # GuiService.ButtonElement(GuiService.GuiSpaces.SCREEN, self.camera, (300, 200))
        #self.rect = GuiService.DraggableRect(GuiService.GuiSpaces.WORLD, self.camera, (-50, 100), (0, 0, 255), (100, 100))
        
        # self.sprite = GuiService.AnimatedSprite(GuiService.GuiSpaces.SCREEN, self.camera, (100,100), "spritestack.png", 1, 8, 16, 16)
        # self.sprite.set_sprite(0)
        # self.sprites = self.sprite.get_sprites()
    
        #self.sprite_stack2 = GuiService.SpriteStack(GuiService.GuiSpaces.WORLD, self.camera, (640, 360), "crate.png", pygame.Rect(16, 1, 16, 16), scale_by=5, stack_spacing=20)

        #self.extra_camera = CameraModule.CameraComponent(pygame.Rect(1180, 620, 80, 80))


    def on_enter(self):
        super().on_enter()


    def update(self):
        pass
        
        
        # mouse_x, mouse_y = pygame.mouse.get_pos()
        # rel_x, rel_y = mouse_x - self.sprite_stack2.position[0], mouse_y - self.sprite_stack2.position[1]
        
        # self.sprite_stack2.set_angle((180 / math.pi) * -math.atan2(rel_y, rel_x))
        
        
        # print(f"world pos: {self.rect.world_position}")
        # print(f"screen pos: {self.rect.screen_position}")

    def events(self, event):
        pass


    def draw(self, surface):
        #print("drawing from scene")
        #screen.fill((235, 235, 235))
        surface.fill((227, 192, 109))
        