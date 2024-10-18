import pygame, sys, os, random
pygame.init()


class Main:

    def __init__(self) ->None:
        super().__init__()
        self.display = pygame.display.set_mode((1280, 720))
        self.run = True
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            pass

    def update(self):
        pass

    def draw(self):
        """Custom drawing logic here"""
        import math
        self.display.fill((20, 100, 180))
        pygame.display.flip()

    def test_run(self):
        """Handles the running of the game"""
        while self.run:
            self.clock.tick()
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()


game = Main()
game.test_run()
