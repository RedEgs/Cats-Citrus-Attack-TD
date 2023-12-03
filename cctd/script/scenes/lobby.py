import pytweening, pygame, json, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.gui import *
from ..libs.utils import *
from ..libs.scenes import *
from ..libs.map import *


class LobbyScene(Scene):
    def __init__(self, screen, registry, scene_director, scene_name):
        super().__init__(screen, scene_director, scene_name)

        self.screen = screen
        self.registry = registry
        self.scene_director = scene_director
        self.scene_name = scene_name
        
        self.map_director = MapDirector(screen)

        self.width, self.height = self.screen.get_size()
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        
        self.current_selected_index = 0
        
        self.playButton = Button(
            self.center_x, self.center_y+200, os.path.join(resources_dir, "lobby", "endless_button_off.png"), os.path.join(resources_dir, "lobby", "endless_button_on.png"), self.playGame)
        self.background = pygame.image.load(
            os.path.join(resources_dir, "lobby", "background.png")).convert_alpha()

    def load_towers(self):
        towers_data = self.registry.get_towers_data()
        
        self.tower_items = []  
        
        for tower_data in towers_data:
            image = pygame.image.load(os.path.join(current_dir, '..', '..', 'resources', 'lobby',f'tower_select_{check_rarity_color(tower_data["base_rarity"])}.png')).convert_alpha()
            cover = pygame.image.load(os.path.join(current_dir, '..', '..', 'towers', tower_data["id"], f'cover.png')).convert_alpha()
           
            cover_pos = cover.get_rect(center=(image.get_width()//2, image.get_height()//2))
            image.blit(cover, cover_pos)
            
            self.tower_items.append((image, self.calculate_positions(towers_data.index(tower_data))))
            
        return self.tower_items    
            
    def calculate_positions(self, i):
        item_pos = (107+(113+44)*i,110)

        return item_pos


    def playGame(self):
        self.scene_director.switch_scene("game_scene")

    def on_exit(self):
        return super().on_exit()

    def on_enter(self):
        return super().on_enter()
    
    def events(self, event):
        self.playButton.handle_event(event)

    def update(self):
        self.playButton.update()

    def draw(self):

        
        self.screen.fill(0)
        
        self.screen.blit(self.background, (0,0))
        self.playButton.draw(self.screen)
        
        for tower_item in self.load_towers():
            self.screen.blit(tower_item[0], tower_item[1]) 
            
    def run(self, event):
        self.events(event)
        self.update()
        self.draw()

    def get_scene_info(self):
        return self.scene_name