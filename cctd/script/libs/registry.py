import pytweening, pydantic, pygame, json, sys, os
from pydantic import BaseModel, DirectoryPath


current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.map import *
from ..libs.gui import *
from ..libs.utils import *

class Registry:
    def __init__(self):
        self.tower_registry = []
        self.enemy_registry = []

    def load_tower_registry(self):
        tower_dir = "cctd/towers"
        tower_list = os.listdir(tower_dir)
        
        for tower in tower_list:
            self.tower_registry.append(tower)

    def load_enemy_registry(self):
        pass
    
    def get_tower_registry(self):
        return self.tower_registry
    
    def get_towers_data(self):
        towers_data = []
    
        for tower in self.get_tower_registry():
            tower_data_file = open(os.path.join(current_dir, '..', '..', 'towers', tower, "tower_data.json"), "r")
            tower_json = tower_data_file.read()
            tower_data_file.close()
    
            tower_data = json.loads(tower_json)
            
            #print(tower_data)
            towers_data.append(tower_data)
            
        return towers_data
            
    def get_tower_cover(self):
        tower_covers = []
        for tower in self.get_tower_registry():
            tower_cover = os.path.join(current_dir, '..', '..', 'towers', tower, 'cover.png')
            tower_covers.append(tower_cover)
        
        return tower_covers
        
    def get_towers_sprite(self):
        tower_sprites = []
        for tower in self.get_tower_registry():
            tower_cover = os.path.join(current_dir, '..', '..', 'towers', tower, 'sprite.png')
            tower_sprites.append(tower_cover)
        
        return tower_sprites
        
    