import pygame
import pygame.math as pma


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        pygame.sprite.Sprite.__init__(self)

        self.x = int(x)
        self.y = int(y)
        self.velX = 0
        self.velY = 0

        self.directionVector = pma.Vector2((0, -1))
        self.velocity = 0  # Initial velocity
        self.max_velocity = 3  # Maximum speed
        self.acceleration = 0.1  # Acceleration rate

        self.color = (250, 120, 60)

        self.originalImage = pygame.image.load("player.png")
        self.image = self.originalImage
        self.rect = self.image.get_rect(center=(self.x, self.y))
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

    def move(self):
        keys = pygame.key.get_pressed()

        # Reset velocity to 0
        self.velX = 0
        self.velY = 0

        # Update velocity using lerping
        if keys[pygame.K_w]:
            self.velY = -self.velocity
        elif keys[pygame.K_s]:
            self.velY = self.velocity
        if keys[pygame.K_a]:
            self.velX = -self.velocity
        elif keys[pygame.K_d]:
            self.velX = self.velocity

        # Lerping (smoothly increase velocity)
        target_velocity = self.max_velocity if any(
            [keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]]) else 0
        self.velocity += (target_velocity - self.velocity) * self.acceleration

        # Calculate movement based on velocity
        self.rect.x += self.velX
        self.rect.y += self.velY

        self.point_at(*pygame.mouse.get_pos())
