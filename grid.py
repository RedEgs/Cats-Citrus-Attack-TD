# grid.py

import pygame
import sys

DefaultColor = (255, 255, 255)
GridColor = (100, 100, 100)


class GridCell:
    def __init__(self, x, y, cell_size):
        self.x = x  # x position in grid
        self.y = y  # y position in grid
        self.cell_size = cell_size
        self.selected = False  # Whether the cell is selected
        self.hovered = False   # Whether the mouse is hovering over the cell
        self.visible = True    # Whether the cell is visible

    def draw(self, screen):
        if self.visible:
            if self.selected:
                color = (0, 255, 0)  # Green if selected
            elif self.hovered:
                color = (255, 0, 0)  # Red if hovered
            else:
                color = DefaultColor  # White otherwise

            pygame.draw.rect(screen, color, (self.x * self.cell_size,
                             self.y * self.cell_size, self.cell_size, self.cell_size))
            pygame.draw.rect(screen, GridColor, (self.x * self.cell_size,
                             self.y * self.cell_size, self.cell_size, self.cell_size), 1)

    def toggle_select(self):
        self.selected = not self.selected

    def is_hovered(self, mouse_x, mouse_y):
        cell_x, cell_y = self.x * self.cell_size, self.y * self.cell_size
        return cell_x <= mouse_x < cell_x + self.cell_size and cell_y <= mouse_y < cell_y + self.cell_size


class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[GridCell(x, y, cell_size)
                      for x in range(width)] for y in range(height)]

        # Camera properties
        self.camera_x = 0  # Initial camera position x
        self.camera_y = 0  # Initial camera position y
        self.zoom = 1.0    # Initial zoom level

        # Variables for click-and-drag camera movement
        self.is_dragging = False
        self.prev_mouse_pos = None

    def draw(self, screen):
        for row in self.grid:
            for cell in row:
                cell.draw(screen)

        # Draw grid lines based on camera position and zoom
        for x in range(int(self.camera_x), int(self.camera_x + self.width * self.cell_size * self.zoom), int(self.cell_size * self.zoom)):
            pygame.draw.line(screen, GridColor, (x - self.camera_x, 0),
                             (x - self.camera_x, self.height * self.cell_size * self.zoom))
        for y in range(int(self.camera_y), int(self.camera_y + self.height * self.cell_size * self.zoom), int(self.cell_size * self.zoom)):
            pygame.draw.line(screen, GridColor, (0, y - self.camera_y),
                             (self.width * self.cell_size * self.zoom, y - self.camera_y))

    def toggle_cell(self, x, y):
        self.grid[y][x].toggle_select()

    def update_hover(self, mouse_x, mouse_y):
        for row in self.grid:
            for cell in row:
                cell.hovered = cell.is_hovered(
                    mouse_x / self.zoom + self.camera_x, mouse_y / self.zoom + self.camera_y)

    def start_drag(self, mouse_x, mouse_y):
        self.is_dragging = True
        self.prev_mouse_pos = (mouse_x, mouse_y)

    def stop_drag(self):
        self.is_dragging = False

    def drag_camera(self, mouse_x, mouse_y):
        if self.is_dragging and self.prev_mouse_pos:
            dx = (mouse_x - self.prev_mouse_pos[0]) / self.zoom
            dy = (mouse_y - self.prev_mouse_pos[1]) / self.zoom
            self.camera_x += dx
            self.camera_y += dy
            self.prev_mouse_pos = (mouse_x, mouse_y)


def positionOnGrid(mouseX, mouseY, cellSize):
    """
    Gets The Mouse Position Relative to the Grid
    """
    gridX = mouseX // cellSize
    gridY = mouseY // cellSize

    return gridX, gridY
