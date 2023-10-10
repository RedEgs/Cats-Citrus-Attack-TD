import pygame
import sys
import numpy


class Camera:
    def __init__(self, screen):

        self.screen = screen
        self.width, self.height = screen.get_size()
        self.camera = pygame.Rect(0, 0, self.width, self.height)

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Limit scrolling to the map size
        x = min(0, x)  # Left
        y = min(0, y)  # Top
        x = max(-(self.width - target.screen.get_width()), x)  # Right
        y = max(-(self.height - target.screen.get_height()), y)  # Bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)
