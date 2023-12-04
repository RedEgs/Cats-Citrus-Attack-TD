import pygame, pytweening, sys, os

# Imported global libs

from cctd.script.libs.tween import *


# Pygame setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Tweening Example")

# Image setup

# Tween setup


start_value = (100,00)
end_value = (300,300)

tween_data = TweenDataVector2(start_value=start_value, end_value=end_value, duration=2, delay=0, easing_function=pytweening.easeInOutElastic)
tween = TweenVector2(tween_data)


running = True
tween.start()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    
    
    image = pygame.Surface((50, 50))
    image.fill((255, 0, 0))  # Red square

    
    
    
    tween.update()
    
    
    
    screen.blit(image, (tween.get_output()))  
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
