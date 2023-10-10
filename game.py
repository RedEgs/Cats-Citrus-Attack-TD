import pygame
import sys
from grid import *
from camera import *
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

        self.camera = Camera(screen)
        self.player = Player(screen)

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
            elif event.type == pygame.KEYDOWN:
                if event.key in self.player.keys:
                    self.player.keys[event.key] = True

            if event.type == pygame.KEYUP:
                if event.key in self.player.keys:
                    self.player.keys[event.key] = False

    def update(self):
        self.fpsCounter.update()
        self.player.update()
        self.player.handle_input()

        self.camera.update(self.player)

        pass

    def draw(self):
        self.screen.fill((0, 0, 0))

        # Draw the Grid
        self.grid.draw(self.screen)

        # Debugging
        self.fpsCounter.draw()
        self.gridDebug.draw()

        # Camera Stuff
        player_position = self.camera.apply(self.player)
        self.player.x, self.player.y = player_position.topleft
        self.player.draw()

        # TODO - FIX THE CAMERA. MAKE THE CAMERA FOLLOW THE PLAYER

        # Player

        # Update The Display
        pygame.display.update()
