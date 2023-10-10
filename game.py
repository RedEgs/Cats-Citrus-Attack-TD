import pygame
import sys
from grid import *
from player import *
from debugs import *

FPS = 60  # Set Constant FPS
cellSize = 20


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.grid = Grid(50, 50, 20)

        self.fpsCounter = FPSCounter(screen, clock)
        self.gridDebug = GridDebug(screen)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        gridX, gridY = positionOnGrid(mouseX, mouseY, cellSize)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit Event
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.grid.toggle_cell(gridX, gridY)

                    print(f"Clicked on cell at position ({gridX}, {gridY})")
            elif event.type == pygame.MOUSEMOTION:
                self.grid.update_hover(mouseX, mouseY)
                self.gridDebug.update(
                    gridX, gridY, self.grid.get_hovered_cell(mouseX, mouseY).selected)

                # Handle player movement
    def update(self):
        self.fpsCounter.update()

        pass

    def draw(self):
        self.screen.fill((0, 0, 0))

        # Draw the Grid
        self.grid.draw(self.screen)

        # Debugging
        self.fpsCounter.draw()
        self.gridDebug.draw()

        # Update The Display
        pygame.display.update()
