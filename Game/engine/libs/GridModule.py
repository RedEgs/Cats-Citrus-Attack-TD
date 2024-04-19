import pytweening, pygame, time, sys, os
import numpy as np


class Grid:
    def __init__(self, grid_size: int, cell_size: int) -> None:
        """
        Grid generates a square array, which can then be used for whatever
        """
        self.grid = np.zeros((grid_size, grid_size), dtype=int)
        
        self.grid_size = grid_size
        self.grid_width = self.grid_size 
        self.grid_height = self.grid_size
        self.cell_size = cell_size
        
    def cell_to_pixel(self, x, y):
        return x * self.cell_size, y * self.cell_size
    
    def pixel_to_cell(self, x, y):
        return x // self.cell_size, y // self.cell_size
    
    def set_cell_data(self, x, y, data: int):
        self.grid[x, y] = data
        
    def get_cell_data(self, x, y):
        return self.grid[x, y]
    
    def pre_render_grid(self, colorkey: pygame.Color = (0,0,0)) -> pygame.Surface:
        """
        Pre-render the grid onto a separate surface
        """
        grid_surface = pygame.Surface((self.grid_width * self.cell_size, self.grid_height * self.cell_size))
        grid_surface.fill(colorkey)
        grid_surface.set_alpha(80)
        
        for x in range(0, self.grid_width * self.cell_size, self.cell_size):
            pygame.draw.line(grid_surface, (255,255,255), (x, 0), (x, self.grid_height * self.cell_size))
        for y in range(0, self.grid_height * self.cell_size, self.cell_size):
            pygame.draw.line(grid_surface, (255,255,255), (0, y), (self.grid_width * self.cell_size, y))
        return grid_surface
    
    def draw_to_surface(self, surface: pygame.Surface, color: pygame.Color = (230, 230, 180)) -> None:
        """
        Draw the grid onto a Pygame surface
        """
        for x in range(0, self.grid_width * self.cell_size, self.cell_size):
            pygame.draw.line(surface, pygame.Color("black"), (x, 0), (x, self.grid_height * self.cell_size))
        for y in range(0, self.grid_height * self.cell_size, self.cell_size):
            pygame.draw.line(surface, pygame.Color("black"), (0, y), (self.grid_width * self.cell_size, y))