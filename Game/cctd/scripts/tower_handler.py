import pytweening, pygame, sys, os, math

import engine.libs.Formatter as formatter
import engine.libs.Utils as utils
import engine.libs.EntityService as EntityService 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService


class TowerHandler:
    def __init__(self, app, map):
        #self.registry = app.registry_service
        self.map = map

        self.towers = pygame.sprite.Group()
        self.towers_amount = len(self.towers)
        self.towers_limit = 5

        self.selected_tower = None

        self.click_state = False

    def place(self):
        max_size = (1920,1080)



        self.towers.add(new_tower)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left Click
            self.click_state = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.click_state == True:
                self.click_state = False
                self.place()



    def update(self):
        for tower in self.towers.sprites():
            tower.update()
            
    def draw(self, screen):
        self.towers.draw(screen)

    def get_towers(self):
        return self.towers
   

class Tower(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()  # Call the superclass constructor  
        self.file_path = f"cctd/towers/example_hero"
        self.sprite_path = f"{self.file_path}/sprite.png"

        self.image = pygame.image.load(self.sprite_path).convert_alpha()  # Use 'image' instead of 'sprite' for clarity
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.mask = pygame.mask.Mask((self.rect.width, self.rect.height))
        self.mask.fill()

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Use 'blit' to draw the image on the screen

    def get_sprite(self):
        return self.image  # Use 'image' instead of 'sprite' for consistency

    def get_mask(self):
        return self.mask

    def get_rect(self):
        return self.rect
