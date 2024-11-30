# grid.py
import pygame
from pygame import math

DefaultColor = (38, 41, 46)
HighlightColor = (80, 87, 97)


class GridCell:
    def __init__(self, x, y, cell_size):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.hovered = False
        self.visible = True

    def draw(self, screen, toggle):
        if self.visible:
            if self.hovered & toggle:
                color = HighlightColor
            else:
                color = DefaultColor

            pygame.draw.rect(screen, color, (self.x * self.cell_size,
                             self.y * self.cell_size, self.cell_size, self.cell_size))

    def is_hovered(self, mouse_x, mouse_y):
        cell_x, cell_y = self.x * self.cell_size, self.y * self.cell_size
        return cell_x <= mouse_x < cell_x + self.cell_size and cell_y <= mouse_y < cell_y + self.cell_size


class Grid:
    def __init__(self, cell_size, render_width, render_height):
        self.cell_size = cell_size
        self.render_width = render_width
        self.render_height = render_height
        self.grid = [[GridCell(x, y, cell_size)
                      for x in range(render_width)] for y in range(render_height)]

    def draw(self, screen):
        for row in self.grid:
            for cell in row:
                if cell.x < self.render_width and cell.y < self.render_height:
                    cell.draw(screen)

    def update_hover(self, mouse_x, mouse_y, grid_overlay_enabled=True):
        if grid_overlay_enabled:
            for row in self.grid:
                for cell in row:
                    if cell.x < self.render_width and cell.y < self.render_height:
                        cell.hovered = cell.is_hovered(mouse_x, mouse_y)
        else:
            # Disable hovering when grid overlay is disabled
            for row in self.grid:
                for cell in row:
                    cell.hovered = False

    def get_hovered_cell(self, mouse_x, mouse_y):
        for row in self.grid:
            for cell in row:
                if cell.is_hovered(mouse_x, mouse_y):
                    return cell
        return None

    def draw_within_map_bounds(self, screen, map_width, map_height, toggle):
        for i in range(min(self.render_height, map_height)):
            for j in range(min(self.render_width, map_width)):
                cell = self.grid[i][j]
                cell.draw(screen, toggle)

    def get_grid_res(self):
        return math.Vector2(self.render_width * self.cell_size, self.render_height * self.cell_size)


def positionOnGrid(mouseX, mouseY, cellSize):
    """
    Gets The Mouse Position Relative to the Grid
    """
    gridX = mouseX // cellSize
    gridY = mouseY // cellSize

    return gridX, gridY
