import pytweening, pygame, sys, os, math
from enum import Enum

import engine.libs.Formatter as formatter
import engine.libs.Utils as utils
 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService

class EnemyHandler:
    enemies  = pygame.sprite.Group()

    @classmethod
    def add_enemy(cls, enemy):
        #cls.enemies.append(enemy)
        cls.enemies.add(enemy)
    
    @classmethod
    def update(cls):
        for enemy in cls.enemies.sprites():
            enemy.update()
    
    @classmethod
    def draw(cls, screen):
        cls.enemies.draw(screen)
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self, waypoints):
        pygame.sprite.Sprite.__init__(self)

        self.waypoints = waypoints
        self.pos = pygame.Vector2(self.waypoints[0])
        self.speed = 1

        self.targetPoint = 1

        self.originalImage = pygame.image.load(
            "cctd/resources/enemies/enemy.png").convert_alpha()
        self.image = self.originalImage
        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        EnemyHandler.add_enemy(self)

    def move(self):
        if self.targetPoint < len(self.waypoints):
            self.target = pygame.Vector2(self.waypoints[self.targetPoint])
            self.path = self.target - self.pos  # Assuming self.target and self.pos are vectors or points
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
        self.image = pygame.transform.rotate(self.originalImage, self.angle)
        self.rect.center = self.pos

    def update(self):
        self.move()
        self.rotate()
