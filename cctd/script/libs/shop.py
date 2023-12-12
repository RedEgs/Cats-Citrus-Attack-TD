import pytweening, pygame, random, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.utils import *
from ..libs.registry import *
from ..libs.scenes import *
from ..libs.transitions import *
from ..libs.gui import *
from ..libs.towers import *

class Shop():
    def __init__(self, registry : Registry, gui_director : GUIDirector):
        self.gui_director = gui_director
        self.registry = registry

        self.selected_cards = self.registry.get_selected_towers_registry()
        

        
        self.all_items = []
        self.last_added = pygame.time.get_ticks()
        
        


    def add_item(self):
        shop_cooldown = random.randint(3, 5) * 1000
        current_tick = pygame.time.get_ticks()
        
        if current_tick - self.last_added >= shop_cooldown:
            #print("Added item at " + str(current_tick))
            self.last_added = current_tick
            item = shop_item(self.gui_director, self.all_items, self.registry.get_towers_data(self.selected_cards)[get_random_index(self.selected_cards)], self.registry)
        
    
        
    def handle_event(self, event):
        for i in self.all_items:
            i.handle_event(event)
        
    def update(self):
        for i in self.all_items:
            i.update()
        
        if len(self.all_items) != 4:
            self.add_item()
            
        
        
    def draw(self, screen):
        for item in self.all_items:
            item.draw(screen)
        
        
    

class shop_item():
    def __init__(self,  gui_director, list, tower_data, registry : Registry):
        self.gui_director = gui_director
        self.registry = registry

        list.append(self)
        self.shop_item_index = list.index(self)
        self.tower_data = tower_data
        self.rarity = tower_data["base_rarity"]
        self.item_name = tower_data["id"]
        self.item_text = "None"
        self.cost = 0
        self.xp_cost = 0
        self.required_round = 0
        
        self.pos = (622, 75 + 50*self.shop_item_index)
        
        if self.rarity == "uncommon" or self.rarity == 1:
            self.img_path = os.path.join(current_dir, '..', '..', 'resources', 'game_overlay', 'tower_shop_green.png')
            self.outline_color = (29, 102, 39)
        elif self.rarity == "rare" or self.rarity == 2:
            self.img_path = os.path.join(current_dir, '..', '..', 'resources', 'game_overlay', 'tower_shop_blue.png')
            self.outline_color = (48, 76, 121)
        elif self.rarity == "epic" or self.rarity == 3:
            self.outline_color = (80, 59, 132)
            self.img_path = os.path.join(current_dir, '..', '..', 'resources', 'game_overlay', 'tower_shop_purple.png')
        elif self.rarity == "hero" or self.rarity == 4:
            self.img_path = os.path.join(current_dir, '..', '..', 'resources', 'game_overlay', 'tower_shop_red.png')
            self.outline_color = (124, 51, 51)
        else:
            pass    
        
        self.button = Button(self.gui_director, (self.pos[0]+77, self.pos[1]+22), self.img_path, self.img_path, lambda: self.select_tower(), lambda: None)
        
    def select_tower(self):
        print("selected")
        self.registry.selected_tower = self.tower_data

    def get_shop_item(self):
        img = pygame.image.load(self.img_path)
        
        text_object = GUIText(14, (255,255,255), (10 , 10))
        text = text_object.normal_text(self.item_name)
        
        text_object.draw(img)
        
        return img
        
    def handle_event(self, event):  
        self.button.handle_event(event)
        
    def update(self):
        #self.button.update()
        pass
        
        
    def draw(self, screen):
        screen.blit(self.get_shop_item(), self.pos)    

        
    
    
    
