import pygame, sys, os

# Imported global libs



from cctd.script.libs.scenes import *
from cctd.script.libs.utils import *

from cctd.script.scenes.menu import Menu

pygame.init()
pygame.mixer.init()


# Window constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # Window Height Constants
pygame.display.set_caption("Citrus Cats TD")  # Set Window Title
pygame.display.set_icon(pygame.image.load(
    "cctd/resources/constant/ico.png"))  # Window icon

FPS = 120  # FPS Limit
clock = pygame.time.Clock()  # Program clock
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT))  # Screen initialisation


class Main:
    def __init__(self):
        self.SceneDirector = SceneDirector("main_menu")

        game_scenes = []
        game_scenes.append(Menu(screen, self.SceneDirector, "main_menu"))
        # Game(self.SCREEN, self.SceneDirector, "debug_scene")
        self.SceneDirector.load_scenes(game_scenes)

    def run(self):
        while True:
            clock.tick(FPS)
            delta_time = clock.tick(FPS) / 1000.0

            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.eventQueue = event

    def update(self):
        self.SceneDirector.run_scene(self.eventQueue)

    def draw(self):
        pygame.display.flip()


if __name__ == "__main__":
    main = Main()
    main.run()
