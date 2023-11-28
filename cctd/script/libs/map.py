import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.scenes import *

COORDINATE_TOLERANCE = 5  # Adjust this value based on your needs

class Map:
    def __init__(self, filepath, render_width, render_height):
        self.grid, self.map_mask = self.load_map(
            filename, render_width, render_height)
        self.waypoints = []

    def load_map(self, filename, render_width, render_height):
        map_image = pygame.image.load(filename).convert_alpha()
        map_mask_image = pygame.image.load("mask.png").convert_alpha()

        map_mask_rect = map_mask_image.get_rect()
        map_mask = pygame.mask.from_surface(map_mask_image)

        return map_image, map_mask

    def load_waypoints(self, filename):
        with open(filename, 'r') as file:
            waypoints_str = file.read()
            self.waypoints = ast.literal_eval(waypoints_str)

    def draw(self, screen):
        screen.blit(self.grid, (0, 0))

    def save_map(self, filename):
        with open(filename, 'w') as file:
            file.write("[\n")
            for waypoint in self.waypoints:
                file.write(f"    {waypoint},\n")
            file.write("]\n")

    def add_waypoint(self, coordinates):
        self.waypoints.append(coordinates)

    def remove_waypoint(self, coordinates):
        # Remove waypoints that are within the tolerance range
        self.waypoints = [wp for wp in self.waypoints if self.distance_squared(
            coordinates, wp) > COORDINATE_TOLERANCE**2]

    def distance_squared(self, point1, point2):
        return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2

    def get_rounded_coordinates(self, mouse_x, mouse_y):
        gridX, gridY = positionOnGrid(mouse_x, mouse_y, 1)
        rounded_x = round(gridX * 1)
        rounded_y = round(gridY * 1)
        return rounded_x, rounded_y
