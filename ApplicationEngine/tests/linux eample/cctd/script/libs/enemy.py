import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.scenes import *
from ..libs.map import *
from ..libs.gui import *

# enemy_sprite =
class EnemyDirector:
    def __init__(self):
        self.enemy_sprite_group = pygame.sprite.Group()
        self.enemies = []
        
        self.round_count = 0
        self.alive_count = 0
        self.dead_count = 0
    
    def update(self):
        self.enemy_sprite_group.update()
    
    def draw(self, screen):
        self.enemy_sprite_group.draw()

class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoints):
        pg.sprite.Sprite.__init__(self)

        self.waypoints = waypoints
        self.speed = 1
        self.pos = Vector2(self.waypoints[0])

        self.targetPoint = 1

        self.originalImage = pg.image.load(
            "enemy.png").convert_alpha()
        self.image = pg.image.load(
            "enemy.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def move(self):
        if self.targetPoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.targetPoint])
            self.path = self.target - self.pos
        else:
            self.kill()

        distance = self.path.length()
        if distance >= self.speed:
            self.pos += self.path.normalize() * self.speed
        else:
            if distance != 0:
                self.pos += self.path.normalize() * distance
            self.targetPoint += 1

    def rotate(self):
        distance = self.target - self.pos

        self.angle = math.degrees(math.atan2(-distance[1], distance[0]))
        self.image = pg.transform.rotate(self.originalImage, self.angle)
        self.rect.center = self.pos

    def update(self):
        self.move()
        self.rotate()
