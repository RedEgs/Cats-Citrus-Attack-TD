import pygame
import sys


class FPSCounter:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.Font(None, 36)
        self.fps = 0

        self.width, self.height = self.screen.get_size()

        self.text_color = (255, 255, 255, 20)

    def update(self):
        self.fps = int(self.clock.get_fps())

    def draw(self):
        fps_text = self.font.render(f"FPS: {self.fps}", True, self.text_color)
        self.screen.blit(fps_text, (self.width - 100, 10))


class GridDebug:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        # RGBA color with 128 (out of 255) alpha
        self.text_color = (255, 255, 255, 20)

    def update(self, x, y, is_selected):
        self.debug_text = f"Grid Coords: {x},{y} Selected: {is_selected}"

    def draw(self):
        debug_text_render = self.font.render(
            self.debug_text, True, self.text_color)
        self.screen.blit(debug_text_render, (10, 10))
