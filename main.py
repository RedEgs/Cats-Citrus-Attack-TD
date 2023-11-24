import pygame, sys
from game import *
from menu import *

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
    pygame.display.set_caption("Citrus Cats TD") # Set Window Title

    menu = Menu(SCREEN, clock)
    game = Game(SCREEN, clock)
    


    while running:

        menu.run()







        # Menu Goes here

        while playing:

            # Game Loop Here

            game.run()

if __name__ == "__main__":
    main()