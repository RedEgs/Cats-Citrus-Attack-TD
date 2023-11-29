import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.scenes import *
from ..libs.map import *
from ..libs.gui import *
from ..libs.utils import *
class Tower(pygame.sprite.Sprite):
    def __init__(self, tower_director):
        pygame.sprite.Sprite.__init__(self)

        self.tower_director = tower_director
        self.image = pygame.image.load(os.path.join(current_dir, '..', '..', 'resources', 'towers', 'tower.png')).convert_alpha()
        self.rect = self.image.get_rect()
        # self.rect.center = pos

    def place_tower(self, pos):
        print(pos)
        self.rect.center = pos
        self.tower_director.add_tower(self)
        
    def draw(self, screen):
        pygame.draw(screen, (0, 255, 00), self.rect)

    def get_rect(self):
        return self.rect

class TowerDirector:
    def __init__(self, map):
        self.mousePreview = MousePreviewOverlay((48,48), os.path.join(current_dir, '..', '..', 'resources', 'towers', 'tower.png'), 100)
        self.map = map
        
        self.tower_sprite_group = pygame.sprite.Group()
        self.towers = []
        
        self.towers_limit = 4
        self.towers_placed = 0
        self.towers = []  
        self.click = False
        
    def add_tower(self, tower):
        if self.towers_placed != self.towers_limit:
            self.tower_sprite_group.add(tower)
            self.towers.append(tower)
            self.towers_placed += 1
        else:
            print("Reached tower limit")
         
    def handle_event(self, event):        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.click = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.click == True:
                self.click = False
                place_tower(self, self.mousePreview, self.map.get_mask(), self.tower_sprite_group)    
        
        elif event.type == pygame.MOUSEMOTION:
            self.mousePreview.update_position()        
            
    def update(self):
        self.mousePreview.update()
        self.tower_sprite_group.update()
        
    
    def draw(self, screen):
        self.tower_sprite_group.draw(screen)
        self.mousePreview.draw(screen, self.tower_sprite_group, self.map.get_mask())
        

def place_tower(tower_director, preview_tower, mask, group):
    max_width = 600
    max_height = 600

    new_tower = Tower(tower_director)

    # Check collision with other towers
    if not pygame.sprite.spritecollideany(preview_tower, group):

        # Get the rect of the preview tower
        preview_rect = preview_tower.get_rect()

        # Create a mask for the preview tower
        preview_mask = pygame.mask.from_surface(preview_tower.image)

        # Check collision with the mask
        if mask.overlap(preview_mask, (int(preview_rect.x), int(preview_rect.y))) is None:
            # Check if the tower position exceeds the specified limits
            if pygame.mouse.get_pos()[0] <= max_width and pygame.mouse.get_pos()[1] <= max_height:
                new_tower.place_tower(pygame.mouse.get_pos())
                return new_tower  # Return the placed tower
            else:
                print("Tower placed outside of the 600x600 limits.")

class MousePreviewOverlay(pygame.sprite.Sprite):
    def __init__(self, rect_size, image_path, alpha):
        pygame.sprite.Sprite.__init__(self)

        self.width, self.height = rect_size
        self.alpha = alpha

        # Create a rect attribute
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect_x = 0
        self.rect_y = 0

        # Load the image
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))

        # Set the rect position based on the initial values
        self.rect.topleft = (self.rect_x, self.rect_y)

    def update_position(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect_x, self.rect_y = mouse_x - self.width / 2, mouse_y - self.height / 2

        # Update the rect's position
        self.rect.topleft = (self.rect_x, self.rect_y)

    def check_bounds(self):
        if pygame.mouse.get_pos()[0] <= 600 and pygame.mouse.get_pos()[1] <= 600:
            return True

        return False

    def check_conditions(self, tower_group, mask):
        default_color = (255, 0, 0)

        # Create a copy of the image to avoid modifying the original
        tinted_image = self.image.copy()

        # Check collision with other towers
        if not pygame.sprite.spritecollideany(self, tower_group):

            # Get the rect of the preview tower
            preview_rect = self.get_rect()

            # Create a mask for the preview tower
            preview_mask = pygame.mask.from_surface(self.image)

            # Check collision with the mask
            if mask.overlap(preview_mask, (int(preview_rect.x), int(preview_rect.y))) is None:
                # Check if the tower position exceeds the specified limits
                if pygame.mouse.get_pos()[0] <= 600 and pygame.mouse.get_pos()[1] <= 600:
                    default_color = (0, 255, 0)

                    tinted_image.fill((*default_color, self.alpha),
                                      special_flags=pygame.BLEND_RGBA_MULT)

        tinted_image.fill((*default_color, self.alpha),
                          special_flags=pygame.BLEND_RGBA_MULT)

        return tinted_image

    def draw(self, screen, tower_group, mask):
        if self.check_bounds():
            tinted_image = self.check_conditions(tower_group, mask)
            screen.blit(tinted_image, self.rect.topleft)

    def get_rect(self):
        return self.rect

