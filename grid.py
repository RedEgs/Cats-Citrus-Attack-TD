# grid.py
import pygame

DefaultColor = (38, 41, 46)
GridColor = (50, 54, 61)
HighlightColor = (80, 87, 97)

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
                color = HighlightColor  # Use HighlightColor if hovered
            else:
                color = DefaultColor  # White otherwise

            # Draw a thin border (line) around the cell
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

    def draw(self, screen):
        for row in self.grid:
            for cell in row:
                cell.draw(screen)

        # Draw grid lines
        for x in range(0, self.width * self.cell_size, self.cell_size):
            pygame.draw.line(screen, GridColor, (x, 0),
                             (x, self.height * self.cell_size))
        for y in range(0, self.height * self.cell_size, self.cell_size):
            pygame.draw.line(screen, GridColor, (0, y),
                             (self.width * self.cell_size, y))

    def toggle_cell(self, x, y):
        if 0 <= x < self.height and 0 <= y < self.width:
            print(f"x: {x}")
            print(f"y: {y}")
            self.grid[y][x].toggle_select()
        else:
            print(f"Invalid cell coordinates: ({x}, {y})")

    def update_hover(self, mouse_x, mouse_y):
        for row in self.grid:
            for cell in row:
                cell.hovered = cell.is_hovered(mouse_x, mouse_y)

    def get_hovered_cell(self, mouse_x, mouse_y):
        for row in self.grid:
            for cell in row:
                if cell.is_hovered(mouse_x, mouse_y):
                    return cell
        return None  # Return None if no cell is hovered


def positionOnGrid(mouseX, mouseY, cellSize):
    """
    Gets The Mouse Position Relative to the Grid
    """
    gridX = mouseX // cellSize
    gridY = mouseY // cellSize

    return gridX, gridY
