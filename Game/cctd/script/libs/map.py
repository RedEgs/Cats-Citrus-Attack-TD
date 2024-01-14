import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')
map_dir = os.path.join(current_dir, '..', '..', '..', 'maps')

from ..libs.scenes import *
from ..libs.utils import *

COORDINATE_TOLERANCE = 5  # Adjust this value based on your needs

class MapDirector:
    def __init__(self, screen):
        self.all_maps = self.get_available_maps()
        self.loaded_map = None

    def load_map(self, folder_path):
        print("LOADING MAP")
        self.loaded_map = Map(folder_path)
        print("LOADED MAP")

        return self.loaded_map
        
    def get_loaded_map(self):
        return self.loaded_map
        
    def get_available_maps(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        map_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'maps'))
        map_folders = [os.path.join(map_dir, d) for d in os.listdir(map_dir) if os.path.isdir(os.path.join(map_dir, d))]
        return map_folders

class Map:
    def __init__(self, map_folder):
        self.map_folder = map_folder
        self.map_image, self.map_mask = self.load_map()
        self.waypoints = []

    def load_map(self):
        map_path = os.path.join(self.map_folder, 'map.png')
        mask_path = os.path.join(self.map_folder, 'mask.png')

        map_image = pygame.image.load(map_path).convert_alpha()
        map_mask_image = pygame.image.load(mask_path).convert_alpha()

        map_mask_rect = map_mask_image.get_rect()
        map_mask = pygame.mask.from_surface(map_mask_image)

        return map_image, map_mask

    def draw(self, screen):
        screen.blit(self.map_image, (0, 0))

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
        self.waypoints = [wp for wp in self.waypoints if distance_squared(
            coordinates, wp) > COORDINATE_TOLERANCE**2]

    def get_mask(self):
        return self.map_mask


