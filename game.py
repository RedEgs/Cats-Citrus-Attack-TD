import pygame
import sys
from grid import *
from player import *

FPS = 60  # Set Constant FPS
cellSize = 20


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.grid = Grid(50, 50, 20)
        # self.player = Player()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit Event
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouseX, mouseY = pygame.mouse.get_pos()

                    gridX, gridY = positionOnGrid(mouseX, mouseY, cellSize)
                    self.grid.toggle_cell(gridX, gridY)

                    print(f"Clicked on cell at position ({gridX}, {gridY})")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 2:  # Left mouse button
                        self.grid.start_drag(*event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 2:  # Left mouse button
                        self.grid.stop_drag()

            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.grid.update_hover(mouse_x, mouse_y)

                # Handle player movement

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.grid.draw(self.screen)

        pygame.display.update()
