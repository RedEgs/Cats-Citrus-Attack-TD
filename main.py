import pygame, sys
from game import *
from grid import *

#! End of Imports



def main():
    pygame.init() # Initialize Pygame
    pygame.mixer.init()
    clock = pygame.time.Clock()

    running = True
    playing = True

    #* Window Constants
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 # Window Height Constants
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Create the window height and width
    pygame.display.set_caption("Manufactorio: Satisfaction Edition") # Set Window Title

    game = Game(SCREEN, clock)

    while running:

        # Menu Goes here

        while playing:

            # Game Loop Here

            game.run()

if __name__ == "__main__":
    main()