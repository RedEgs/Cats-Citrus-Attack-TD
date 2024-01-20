import pytweening, pygame, sys, os

import engine.libs.Formatter as formatter
import engine.libs.Utils as utils
import engine.libs.EntityService as EntityService 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService

COORDINATE_TOLERANCE = 5  # Adjust this value based on your needs

class Map_Loader:
    def __init__(self):
        self.all_maps = self.get_available_maps()
        self.loaded_map = None

        self.max_maps = len(self.all_maps)
        self.map_index = 1

        print(self.max_maps)

    def load_map(self):
        folder_path = self.all_maps[self.map_index-1]
        self.loaded_map = Map(folder_path)

        return self.loaded_map
        
    def get_loaded_map(self):
        return self.loaded_map
        
    def get_available_maps(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        map_dir = os.path.abspath(os.path.join(current_dir, '..', 'maps'))
        map_folders = [os.path.join(map_dir, d) for d in os.listdir(map_dir) if os.path.isdir(os.path.join(map_dir, d))]
        return map_folders

class Map:
    def __init__(self, map_folder):
        self.map_folder = map_folder
        self.waypoint_data = self.load_waypoint_data()
        self.map_image, self.map_mask = self.load_map()
    
       

  
    def load_map(self):
        map_path = os.path.join(self.map_folder, 'map.png')
        mask_path = os.path.join(self.map_folder, 'mask.png')

        map_image = pygame.image.load(map_path).convert_alpha()
        
        map_mask_image = pygame.image.load(mask_path).convert_alpha()

        map_mask_rect = map_mask_image.get_rect()
        map_mask = pygame.mask.from_surface(map_mask_image)

        return map_image, map_mask

    def load_waypoint_data(self):
        import json

        # Read data from the JSON file
        with open(f"{self.map_folder}/map_data.json", "r") as json_file:
            data = json.load(json_file)

        # Access the waypoints data
        waypoints = data["waypoints"]

        #print(waypoints)
        return waypoints

    

    def save_map(self, filename):
        with open(filename, 'w') as file:
            file.write("[\n")
            for waypoint in self.waypoints:
                file.write(f"    {waypoint},\n")
            file.write("]\n")

    def add_waypoint(self, coordinates):
        self.waypoints.append(coordinates)

    def distance_squared(self, point1, point2):
        return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2


    def remove_waypoint(self, coordinates):
        # Remove waypoints that are within the tolerance range
        self.waypoints = [wp for wp in self.waypoints if self.distance_squared(
            coordinates, wp) > COORDINATE_TOLERANCE**2]

    def get_mask(self):
        return self.map_mask


