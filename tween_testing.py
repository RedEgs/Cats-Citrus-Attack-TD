import pygame, pytweening, sys, os

# Imported global libs

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from cctd.script.libs.tween import *
from cctd.script.libs.gui import *


# Pygame setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Tweening Example")

# Image setup

# Tween setup




start_value = (100,100)
end_value = (300,300)

tween_data = TweenDataVector2(start_value=start_value, end_value=end_value, duration=2, delay=0, easing_function=pytweening.easeInOutElastic)
tween = TweenVector2(tween_data)


running = True

  
def move_button():
    tween.start()
    

button = NewButton((100, 100),  os.path.join(current_dir, '..', '..', 'resources', 'lobby', 'endless_button_off.png'), 
                    os.path.join(current_dir, '..', '..', 'resources', 'lobby', 'endless_button_off.png'), move_button, callback)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        button.handle_event(event)

    screen.fill((255, 255, 255))
    button.draw(screen, tween.get_output())

    tween.update()
    

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
