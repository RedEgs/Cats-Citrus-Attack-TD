import pygame
import sys

from scenes import *
from menu import *
from game import *
from utils import *
import pytweening

#! End of Imports


class Main:
    def __init__(self):
        pygame.init()  # Initialize Pygame
        pygame.mixer.init()

        FPS = 60
        self.clock = pygame.time.Clock()

        SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # Window Height Constants
        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Citrus Cats TD")  # Set Window Title
        icon = pygame.image.load("ICO.png")
        pygame.display.set_icon(icon)

        self.SceneDirector = SceneDirector("main_menu")

        self.main_menu = Menu(self.SCREEN, self.SceneDirector)
        self.debug_scene = Game(self.SCREEN, self.SceneDirector, self.clock)

        self.states = {"main_menu": self.main_menu,
                       "debug_scene": self.debug_scene}

    def run(self):
        while True:
            delta_time = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.states[self.SceneDirector.get_scene()].run(event)
            pygame.display.flip()


if __name__ == "__main__":
    main = Main()
    main.run()
