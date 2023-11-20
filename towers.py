import pygame as pg


def rect_to_surface(rect):
    # Create a Surface with the dimensions of the Rect
    surface = pg.Surface((rect.width, rect.height), pg.SRCALPHA)

    # Return the created Surface
    return surface


def placeTower(tower_group, preview_tower, mask):
    max_width = 600
    max_height = 600

    new_tower = Tower()

    # Check collision with other towers
    if not pg.sprite.spritecollideany(preview_tower, tower_group):

        # Get the rect of the preview tower
        preview_rect = preview_tower.get_rect()

        # Create a mask for the preview tower
        preview_mask = pg.mask.from_surface(preview_tower.image)

        # Check collision with the mask
        if mask.overlap(preview_mask, (int(preview_rect.x), int(preview_rect.y))) is None:
            # Check if the tower position exceeds the specified limits
            if pg.mouse.get_pos()[0] <= max_width and pg.mouse.get_pos()[1] <= max_height:
                new_tower.placeTower(preview_rect.center)
                tower_group.add(new_tower)
                return new_tower  # Return the placed tower
            else:
                print("Tower placed outside of the 600x600 limits.")


class Tower(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(
            "tower.png").convert_alpha()
        self.rect = self.image.get_rect()
        # self.rect.center = pos

    def placeTower(self, pos):
        self.rect.center = pos

    def draw(self, screen):
        pg.draw(screen, (0, 255, 00), self.rect)

    def get_rect(self):
        return self.rect

   # def placeTower(self, preview_place):
        # if self.rect.colliderect()
