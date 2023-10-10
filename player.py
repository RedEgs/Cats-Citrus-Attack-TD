import pygame
from pygame.math import *
import sys
import numpy


class Player:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        self.x = int(self.width/2)
        self.y = int(self.height/2)
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.color = (250, 120, 60)
        self.velX = 0
        self.velY = 0
        self.acceleration = 0.5  # Normal acceleration
        self.base_speed_acceleration = 1  # Acceleration to reach base speed
        self.friction = 0.05  # Friction to slow down the player
        self.max_speed = 5  # Maximum speed
        self.base_speed = 10  # The speed you want to reach quickly
        self.keys = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False
        }

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        # Apply friction
        friction_multiplier = self.friction * \
            (self.velX**2 + self.velY**2) ** 0.5
        if friction_multiplier > 1:
            friction_multiplier = 1  # Cap friction to prevent reverse movement
        self.velX -= self.velX * friction_multiplier
        self.velY -= self.velY * friction_multiplier

        # Adjust acceleration based on max speed
        if self.velX < -self.max_speed:
            self.velX = -self.max_speed
        if self.velX > self.max_speed:
            self.velX = self.max_speed
        if self.velY < -self.max_speed:
            self.velY = -self.max_speed
        if self.velY > self.max_speed:
            self.velY = self.max_speed

        self.x += self.velX
        self.y += self.velY

        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)

    def handle_input(self):
        for key, value in self.keys.items():
            if value:
                if key == pygame.K_LEFT:
                    if self.velX > -self.base_speed:
                        self.velX -= self.base_speed_acceleration
                    elif self.velX > -self.max_speed:
                        self.velX -= self.acceleration
                elif key == pygame.K_RIGHT:
                    if self.velX < self.base_speed:
                        self.velX += self.base_speed_acceleration
                    elif self.velX < self.max_speed:
                        self.velX += self.acceleration
                elif key == pygame.K_UP:
                    if self.velY > -self.base_speed:
                        self.velY -= self.base_speed_acceleration
                    elif self.velY > -self.max_speed:
                        self.velY -= self.acceleration
                elif key == pygame.K_DOWN:
                    if self.velY < self.base_speed:
                        self.velY += self.base_speed_acceleration
                    elif self.velY < self.max_speed:
                        self.velY += self.acceleration

    def getPosition(self):
        return self.x, self.y
