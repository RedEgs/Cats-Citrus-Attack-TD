# map.py
import pygame
from grid import Grid

cellSize = 20

# map.py
import pygame
from grid import Grid

class Map:
    def __init__(self, filename, width, height):
        self.grid = self.load_map(filename, width, height)

    def load_map(self, filename, width, height):
        with open(filename, 'r') as file:
            lines = file.readlines()
            map_width = max(len(line.strip()) for line in lines)  # Find the maximum length among all lines
            map_height = len(lines)

            map_grid = Grid(width, height, cellSize)

            for i in range(map_height):
                # Pad the line with zeros if its length is less than the maximum length
                padded_line = lines[i].strip().ljust(map_width, '0')

                for j, char in enumerate(padded_line):
                    cell_type = int(char)
                    if cell_type == 1:
                        map_grid.toggle_cell(j, i)

            # Fill the rest of the grid with default squares
            for i in range(map_height, height):
                for j in range(map_width):
                    map_grid.toggle_cell(j, i)

        return map_grid
    
    def save_map(self, filename):
        with open(filename, 'w') as file:
            for row in self.grid.grid:
                # Convert each cell's selected state to 1 or 0 and join them into a string
                line = ''.join(str(int(cell.selected)) for cell in row)
                file.write(line + '\n')