import pygame.math as pma
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, startingVector, screen):
        pygame.sprite.Sprite.__init__(self)
        self.currentVector = pma.Vector2(startingVector)
        self.velocityVector = pma.Vector2()
        self.directionVector = pma.Vector2((0, -1))
        self.velocity = 5

        self.color = (250, 120, 60)

        self.originalImage = pygame.image.load("player.png")
        self.image = self.originalImage
        self.rect = self.image.get_rect(center=self.currentVector)
        self.screen = screen

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        
    def point_at(self, x, y):
        self.direction = pygame.math.Vector2(x, y) - self.rect.center
        angle = self.direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.originalImage, angle)
        self.rect = self.image.get_rect(center=self.rect.center)





