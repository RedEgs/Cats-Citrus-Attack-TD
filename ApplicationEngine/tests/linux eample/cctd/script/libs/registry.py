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

        self.towers_limit = 5
        self.selected_towers = []
        self.selected_tower = None

    def load_tower_registry(self):
        tower_dir = "cctd/towers"
        tower_list = os.listdir(tower_dir)
        
        for tower in tower_list:
            self.tower_registry.append(tower)
        
        self.tower_registry = list(set(self.tower_registry))

    def load_enemy_registry(self):
        pass
    
    def add_to_selected_towers(self, tower):
        if len(self.selected_towers) >= self.towers_limit:
            return print("Reached Selected Tower Limit")
        else:
            self.selected_towers.append(tower)
            
    def remove_selected_towers(self, tower):
        self.selected_towers.remove(tower)
    
    def get_selected_towers_registry(self):
        return self.selected_towers
    
    def get_tower_registry(self):
        return self.tower_registry
    
    def get_towers_data(self, list=None):
        towers_data = []
    
        if list == None:
            list = self.get_tower_registry()

        print(list)
        for tower in list:
            tower_data_file = open(os.path.join(current_dir, '..', '..', 'towers', tower, "tower_data.json"), "r")
            tower_json = tower_data_file.read()
            tower_data_file.close()
    
            tower_data = json.loads(tower_json)
            
            #print(tower_data)
            towers_data.append(tower_data)
            
        return towers_data
     
    def get_towers_dir(self):
        towers_dirs = []
        
        for tower in self.get_tower_registry():
            towers_dirs = open(os.path.join(current_dir, '..', '..', 'towers', tower), "r")

            return towers_dirs

    def get_tower_data(self, tower):

        tower_data_file = open(os.path.join(current_dir, '..', '..', 'towers', tower, "tower_data.json"), "r")
        tower_json = tower_data_file.read()
        tower_data_file.close()

        tower_data = json.loads(tower_json)
        
        #print(tower_data)
         
        return tower_data
        
        

    def get_tower_dir(self, tower):
        try:
            tower_dir = os.path.join(current_dir, '..', '..', 'towers', tower)
        except FileNotFoundError:
            print("Specific tower directory does not exist")
        
        return tower_dir