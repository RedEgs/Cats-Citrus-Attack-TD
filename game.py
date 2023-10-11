import pygame, sys
import pygame.math as pma
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

        
        self.player = Player(pma.Vector2(13, 13), screen)
        self.allSprites = pygame.sprite.Group(self.player)
        
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
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit Event
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.grid.toggle_cell(gridX, gridY)

                    print(f"Clicked on cell at position ({gridX}, {gridY})")
            elif event.type == pygame.MOUSEMOTION:

                self.player.point_at(*event.pos)

                self.grid.update_hover(mouseX, mouseY)
                self.gridDebug.update(
                    gridX, gridY, self.grid.get_hovered_cell(mouseX, mouseY).selected)
            
            self.player.move(keys[pygame.K_d]-keys[pygame.K_a], keys[pygame.K_s]-keys[pygame.K_w])
            self.player.point_at(*pygame.mouse.get_pos())



    def update(self):
        self.fpsCounter.update()
        self.player.update()
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))

        # Draw the Grid
        self.grid.draw(self.screen)

        # Debugging
        self.fpsCounter.draw()
        #self.gridDebug.draw()

        # Player Stuff
        self.allSprites.draw(self.screen)

        # TODO - FIX THE CAMERA. MAKE THE CAMERA FOLLOW THE PLAYER

        # Update The Display
        pygame.display.update()
