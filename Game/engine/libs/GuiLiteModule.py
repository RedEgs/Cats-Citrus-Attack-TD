import pytweening, pygame, time, sys, os, math

import engine.libs.Utils as utils
import engine.libs.ViewportModule as ViewportModule
import engine.libs.CameraModule as CameraModule


class LiteImageButton:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
        
    def set_image(self, image: pygame.Surface):
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def get_image(self) -> pygame.Surface:
        return self.image

    def get_drawable(self):
        return self.image, self.rect