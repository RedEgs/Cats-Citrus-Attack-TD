import pygame
import pygame_gui


class Sidebar:
    def __init__(self, manager):
        self.manager = manager
        self.width = 200  # Adjust the width as needed
        self.height = 600  # Adjust the height as needed

        # Create a panel for the sidebar
        self.sidebar_panel = pygame_gui.elements.UIPanel(
            pygame.Rect((800, 0), (self.width, self.height)),
            starting_height=1,
            manager=self.manager
        )

        # Add any UI elements you want to the sidebar_panel
        # For example, you can add buttons, labels, etc.
        # Example Button:
        self.example_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (180, 30)),
            text='Click me!',
            manager=self.manager,
            container=self.sidebar_panel
        )

    def update(self, time_delta):
        # Add any updates if needed
        pass

    def draw(self, screen):
        # Draw any additional graphics if needed
        pass
