import pytweening, pygame, json, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')



from ..libs.scenes import *
from ..libs.map import *
from ..libs.gui import *
from ..libs.utils import *
from ..libs.registry import *
class TowerDirector:
    def __init__(self, registry : Registry, map : Map):
        self.registry = registry
        self.map = map

        self.towers = []
        self.towers_amount = len(self.towers)
        self.towers_limit = self.registry.towers_limit

        self.tower_group = pygame.sprite.Group()
    
        self.click_state = False


    def place(self, mask, preview_overlay):
        max_size = (600,600)

        new_tower = Tower(self.registry.selected_tower)

        # Check collision with other towers
        if preview_overlay:
            if not pygame.sprite.spritecollideany(preview_overlay, self.tower_group):

                # Get the rect of the preview tower
                preview_rect = preview_overlay.get_rect()

                # Create a mask for the preview tower
                preview_mask = pygame.mask.from_surface(preview_overlay.get_sprite())

                # Check collision with the maskum 
                if mask.overlap(preview_mask, (int(preview_rect.x), int(preview_rect.y))) is None:
                    # Check if the tower position exceeds the specified limits
                    if pygame.mouse.get_pos() <= max_size:
                        new_tower.instance_tower(pygame.mouse.get_pos())
                        
                        self.towers.append(new_tower)
                        self.tower_group.add(new_tower)
                        
                        
                        
                    else:
                        print("Tower placed outside of the 600x600 limits.")

    
    def handle_event(self, event, preview_overlay):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left Click
            self.click_state = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.click_state == True:
                self.click_state = False
                if self.registry.selected_tower is not None:
                    if check_bounds((600,600)) == True:
                        self.place(self.map.get_mask(), preview_overlay)
                    else:
                        pass
                else:
                    print("No tower selected")





    def update(self):
        for tower in self.towers:
            tower.update()
            
    def draw(self, screen):
        self.tower_group.draw(screen)

    def get_tower_group(self):
        return self.tower_group
        
@dataclass
class TowerData():
    # Technical tower data
    id: str # The "technical" name for the tower, not instance specific (should be same as variable name for convention and ease of access).
    name: str # The "pretty" name for the tower. For example, id = example_tower | name = "Example Tower"

    base_rarity: int
    
    # Base tower values
    base_damage: float
    base_cooldown: float
    base_crit_multiplier: float
    base_crit_chance: float
    base_fire_rate: float
    base_cooldown: float
    base_projectile_speed: float
    
    # Variables values
    damage_multiplier: float
    crit_multiplier: float
    crit_chance_multiplier: float
    fire_rate_multiplier: float
    cooldown_reduction_multiplier: float
    projectile_speed_multiplier: float

    global_positive_multiplier: float
    global_negative_multiplier: float

    # Runtime values
    current_buffs: list 
    current_debuffs: list

class Tower(pygame.sprite.Sprite):
    def __init__(self, tower_data: TowerData):
        super().__init__()  # Call the superclass constructor
        self.tower_data = tower_data    
        self.file_path = f"cctd/towers/{tower_data['id']}"
        self.sprite_path = f"{self.file_path}/sprite.png"

        self.image = load_image(self.sprite_path)  # Use 'image' instead of 'sprite' for clarity
        self.rect = self.image.get_rect()

    def instance_tower(self, pos):
        self.rect.center = pos

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Use 'blit' to draw the image on the screen

    def get_sprite(self):
        return self.image  # Use 'image' instead of 'sprite' for consistency

    def get_rect(self):
        return self.rect

class MousePreviewOverlay(pygame.sprite.Sprite):
    def __init__(self, registry : Registry):
        pygame.sprite.Sprite.__init__(self)
        self.registry = registry
        self.placing_tower = False

        self.s_path = None
        self.sprite_path = None
        self.sprite = None

        self.width, self.height = [None, None]
        self.alpha = None

        # Create a rect attribute
        self.rect = None
        self.rect_x, self.rect_y = [None, None]

        # Load the image
        self.sprite = None


    def update(self):
        #print("u")
        if self.registry.selected_tower != None:
            #print("got tower")
            self.placing_tower = True
            self.s_path = f"cctd/towers/{self.registry.selected_tower['id']}"
            self.sprite_path = f"{self.s_path}/sprite.png"
            self.sprite = load_image(self.sprite_path)

            self.width, self.height = self.sprite.get_size()
            self.alpha = 100

            # Create a rect attribute
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            self.rect_x, self.rect_y = [0,0]

            # Load the image
            self.sprite = pygame.transform.scale(
                self.sprite, (self.width, self.height))

            # Set the rect position based on the initial values
            self.rect.topleft = (self.rect_x, self.rect_y)

            self.update_position()

        

        
    def update_position(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect_x, self.rect_y = mouse_x - self.width / 2, mouse_y - self.height / 2

        # Update the rect's position
        self.rect.topleft = (self.rect_x, self.rect_y)

    def check_bounds(self, play_area_size):
        if pygame.mouse.get_pos() <= play_area_size:
            return True

        return False

    def check_conditions(self, tower_group, mask):
        default_color = (255, 0, 0)

        # Create a copy of the image to avoid modifying the original
        tinted_image = self.sprite.copy()

        # Check collision with other towers
        if not pygame.sprite.spritecollideany(self, tower_group):

            # Get the rect of the preview tower
            preview_rect = self.get_rect()

            # Create a mask for the preview tower
            preview_mask = pygame.mask.from_surface(self.sprite)

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
        if self.placing_tower:
            if self.check_bounds((600, 600)):
                tinted_image = self.check_conditions(tower_group, mask)
                screen.blit(tinted_image, self.rect.topleft)
        
                
    def get_rect(self):
        return self.rect

    def get_sprite(self):
        if self.sprite == None:
            print("NO SPRITE FOUND")
            print(self.sprite_path)
        else:    
            return self.sprite

















"""
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

def place_tower(tower_director, preview_tower, mask, group):
    max_size = (600,600)

    new_tower = Tower(tower_director)

    # Check collision with other towers
    if tower_director.placing_tower == True:
        if not pygame.sprite.spritecollideany(preview_tower, group):

            # Get the rect of the preview tower
            preview_rect = preview_tower.get_rect()

            # Create a mask for the preview tower
            preview_mask = pygame.mask.from_surface(preview_tower.image)

            # Check collision with the mask
            if mask.overlap(preview_mask, (int(preview_rect.x), int(preview_rect.y))) is None:
                # Check if the tower position exceeds the specified limits
                if pygame.mouse.get_pos() <= max_size:
                    new_tower.place_tower(pygame.mouse.get_pos())
                    return new_tower  # Return the placed tower
                else:
                    print("Tower placed outside of the 600x600 limits.")

class MousePreviewOverlay(pygame.sprite.Sprite):
    def __init__(self, tower_director, rect_size, image_path):
        pygame.sprite.Sprite.__init__(self)

        self.tower_director = tower_director
        self.width, self.height = rect_size
        self.alpha = 100

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

    def check_bounds(self, play_area_size):
        if pygame.mouse.get_pos() <= play_area_size:
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
        if self.tower_director.placing_tower == True:
            if self.check_bounds((600, 600)):
                tinted_image = self.check_conditions(tower_group, mask)
                screen.blit(tinted_image, self.rect.topleft)

    def get_rect(self):
        return self.rect
"""
