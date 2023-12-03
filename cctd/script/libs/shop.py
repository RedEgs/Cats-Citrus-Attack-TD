import pytweening, pygame, random, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.utils import *
from ..libs.scenes import *
from ..libs.transitions import *
from ..libs.gui import *
from ..libs.towers import *

example_tower = TowerData(
    id="example_tower",
    name="Example",
    base_rarity=1,
    base_damage=1.0, base_cooldown=2.0, base_crit_chance=1.25, 
    base_crit_multiplier=5.0, base_fire_rate=2.0, base_projectile_speed=10.0,
    damage_multiplier=0.0, crit_multiplier=0.0, crit_chance_multiplier=0.0, 
    fire_rate_multiplier=0.0, cooldown_reduction_multiplier=0.0, projectile_speed_multiplier=0.0, 
    global_positive_multiplier=0.0, global_negative_multiplier=0.0, current_buffs=[], current_debuffs=[]
)


class Shop():
    def __init__(self):
        self.last_added = pygame.time.get_ticks()
        
        
        
        
        self.all_items = []
        
        


    def add_item(self):
        shop_cooldown = random.randint(3, 5) * 1000
        current_tick = pygame.time.get_ticks()
        
        if current_tick - self.last_added >= shop_cooldown:
            print("Added item at " + str(current_tick))
            self.last_added = current_tick
            item = shop_item(self.all_items, example_tower, random.randint(1, 3), example_tower.id, example_tower.name, 20, 0, 0)
        
    
        
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
    def __init__(self, list, tower_data, rarity, item_name, item_text, cost, xp_cost, required_round):
        list.append(self)
        self.shop_item_index = list.index(self)
        self.tower_data = tower_data
        self.rarity = rarity
        self.item_name = item_name
        self.item_text = item_text
        self.cost = cost 
        self.xp_cost = cost
        self.required_round = required_round
        
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
        
        self.button = Button(self.pos[0]+77, self.pos[1]+22, self.img_path, self.img_path, self.print_details )
        
    def print_details(self):
        print(f"id: {self.tower_data.id} | index: {self.shop_item_index}")
        
    def get_shop_item(self):
        img = pygame.image.load(self.img_path)
        
        text_object = GUIText(14, (255,255,255), (10 , 10))
        text_object.outline_text(self.item_text, self.outline_color)
        
        text_object.draw(img)
        
        return img
        
    def handle_event(self, event):  
        self.button.handle_event(event)   
        
    def update(self):
        self.button.update()
        
    def draw(self, screen):
        screen.blit(self.get_shop_item(), self.pos)    

        
    
    
    
