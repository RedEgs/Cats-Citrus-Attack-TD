import pytweening, pygame, sys, os, math

import engine.libs.Utils as utils
 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService


class TowerManager():
    tower_group = []
    placed_tower_group = []
    selected_tower = None
    can_place = False
       
    @classmethod
    def add_tower(cls, tower):
        cls.tower_group.append(tower)
      
    @classmethod
    def check_collisions(cls):
        if cls.placed_tower_group is not None:
            for tower in cls.placed_tower_group:
                if tower.rect.collidepoint(pygame.mouse.get_pos()):
                    return False
     
        
    @classmethod
    def draw(cls, surface, map_surface, map_mask, panel_rect):
        if cls.selected_tower:
            cls.selected_tower.preview_rect = cls.selected_tower.preview_placement_sprite.get_rect(center=pygame.mouse.get_pos())
            cls.selected_tower.preview_mask = cls.selected_tower.preview_placement_mask.get_rect(center=pygame.mouse.get_pos())
            cls.selected_tower.draw_preview_image(surface, map_surface, map_mask, panel_rect)
    
        for i in cls.placed_tower_group:
            print(i)
            pygame.draw.rect(surface, (255,0,0, 20), i.rect)


    @classmethod
    def place_tower(cls, map_surface, map_mask, gui_surface):
        print("placed tower")
        if cls.selected_tower is not None:
            cls.placed_tower_group.append(cls.selected_tower)
            cls.selected_tower.place(map_surface, map_mask, gui_surface)

        
    @classmethod
    def get_selected_tower(cls):
        if cls.selected_tower is not None:
            return cls.selected_tower
    
    @classmethod
    def set_selected_tower(cls, tower):
        cls.selected_tower = tower
    
    
class Tower:
    def __init__(self, tower_dir, tower_data, tower_sprite):
        self.tower_dir = tower_dir
        self.tower_data = self.load_json(tower_data)
    
        self.tower_sprite = tower_sprite
        self.rect = self.tower_sprite.get_rect()
        
        self.preview_placement_sprite =  pygame.transform.grayscale(self.tower_sprite)
        self.preview_placement_mask = pygame.mask.from_surface(self.preview_placement_sprite)
    
        self.preview_rect = self.preview_placement_sprite.get_rect()
        self.mask_rect = self.preview_rect
        
        TowerManager.add_tower(self)

    def load_json(self, tower_data):
        import json

        with open(tower_data) as tower_data_file:
            data = json.load(tower_data_file)
            
        return data

    def draw_preview_image(self, surface, map_surface, map_mask, panel_rect):
        self.preview_placement_mask.get_rect(center=pygame.mouse.get_pos())
        
        #pygame.draw.rect(surface, (255,0,0, 20), self.preview_placement_mask.get_rect() )
        
        
        if TowerManager.get_selected_tower() is not None:
            self.preview_placement_mask_offset = pygame.Vector2(pygame.mouse.get_pos())-pygame.Vector2(self.preview_placement_mask.get_size())//2
            
            if self.check_placement(map_surface, map_mask, panel_rect):
                self.preview_placement_sprite.fill((0, 1, 0), None, pygame.BLEND_RGB_ADD)
            else:
                self.preview_placement_sprite.fill((255, 0, 0), None, pygame.BLEND_RGB_MULT)
            
            
            surface.blit(self.preview_placement_sprite, pygame.mouse.get_pos())

    def place(self, map_surface: pygame.Surface, map_mask: pygame.Mask, gui_surface):
        if self.check_placement(map_surface, map_mask, gui_surface):
            self.pos = pygame.mouse.get_pos()
            self.rect = self.tower_sprite.get_rect(center=self.pos)
            
            map_surface.blit(self.tower_sprite, (self.tower_sprite.get_rect(center=(pygame.mouse.get_pos()))))
    
    def check_placement(self, map_surface: pygame.Surface, map_mask: pygame.Mask, rect):
        if TowerManager.get_selected_tower is not None:
            return map_surface.get_rect().collidepoint(pygame.mouse.get_pos()) and not rect.collidepoint(pygame.mouse.get_pos()) and not map_mask.overlap_mask(self.preview_placement_mask, (0,0))

    def open_tower_context(self):
        print("cliekd on tower")

    def is_over(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
        
    def get_drawable(self):
        return self.tower_sprite, self.rect