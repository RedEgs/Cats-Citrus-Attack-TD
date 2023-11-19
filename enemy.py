import pygame as pg
from pygame.math import Vector2
import math
import pytweening


# enemy_sprite =


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
