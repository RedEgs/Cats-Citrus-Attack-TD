import pygame
import pygame_gui
import sys
from map import Map
from debugs import *
import pytweening as pt
from grid import positionOnGrid  # Add this line to import positionOnGrid

FPS = 60  # Set Constant FPS
cellSize = 20

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        # Load the map from a file (adjust the filename, width, and height accordingly)
        self.map = Map('map.txt', self.width // cellSize, self.height // cellSize)

        self.fpsCounter = FPSCounter(screen, clock)

           # Initialize Pygame GUI manager
        self.manager = pygame_gui.UIManager((self.width, self.height))

        # Create a button to toggle the menu
        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 50)),
            text='Toggle Menu',
            object_id="menuToggle",
            manager=self.manager
        )

        # Create a UI container for the side menu
        self.menu_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((200, 0), (200, self.height)),
            manager=self.manager
        )


    def run(self):
        self.playing = True
        while self.playing:
            time_delta = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update(time_delta)
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
                    self.map.grid.toggle_cell(gridX, gridY)
                    print(f"Clicked on cell at position ({gridX}, {gridY})")
            elif event.type == pygame.MOUSEMOTION:
                self.map.grid.update_hover(mouseX, mouseY)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Save the map when Ctrl + S is pressed
                    self.map.save_map('map.txt')
                    print("Saved Map")
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_object_id == "menuToggle":
                    print("Toggle Menu")
                    new_button_position = (500, 40)  # Replace with the desired position
                    self.menu_button.relative_rect.topleft = new_button_position


            # Pass events to Pygame GUI manager
            self.manager.process_events(event)

    def update(self, time_delta):
        self.fpsCounter.update()

        # Update Pygame GUI manager
        self.manager.update(time_delta)


    def draw(self):
        self.screen.fill((0, 0, 0))

        # Draw the Grid from the loaded map
        self.map.grid.draw(self.screen)

        # Debugging
        self.fpsCounter.draw()

        # Draw the GUI using Pygame GUI manager
        self.manager.draw_ui(self.screen)

        # Update The Display
        pygame.display.update()

