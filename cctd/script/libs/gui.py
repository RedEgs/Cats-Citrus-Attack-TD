import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.utils import *
from ..libs.scenes import *
from ..libs.transitions import *
from ..libs.tween import *

pygame.font.init()

class Outliner:
    def __init__(self, thickness_horizontal, thickness_vertical):
        self.convolution_mask = pygame.mask.Mask((thickness_horizontal, thickness_vertical), fill = True)
        self.convolution_mask.set_at((0, 0), value = 0)
        self.convolution_mask.set_at((2, 0), value = 0)
        self.convolution_mask.set_at((0, 2), value = 0)
        self.convolution_mask.set_at((2, 2), value = 0)
    
    def outline_surface(self, surface, color = 'black', outline_only = False):
        mask = pygame.mask.from_surface(surface)
        
        surface_outline = mask.convolve(self.convolution_mask).to_surface(setcolor = color, unsetcolor = surface.get_colorkey())
        
        if outline_only:
            mask_surface = mask.to_surface()
            mask_surface.set_colorkey('black')
            
            surface_outline.blit(mask_surface, (1, 1))
            
        else:
            surface_outline.blit(surface, (1, 1))
        
        return surface_outline

class GUIText:
    def __init__(self, size, color, pos):
        self.color = color
        self.pos = pos
        self.default_font = pygame.font.Font(os.path.join(current_dir, '..', '..', 'resources', 'constant', 'font.ttf'), size)

    def normal_text(self, text):
        self.text = self.default_font.render(text, True, self.color)

    def outline_text(self, text, outline_color):
        outline = Outliner(3, 3)
        self.text = self.default_font.render(text, True, self.color)
        
        
        self.surface = outline.outline_surface(self.text, outline_color)
        self.text = self.surface

    def draw(self, screen):
        screen.blit(self.text, self.pos)

class GUIElement:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class GameOverlay(GUIElement):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)
        self.healthText = None
        self.roundCounter = None



    def draw(self, surface):
        return super().draw(surface)
    
class Button:
    def __init__(self, position, image_off_path, image_on_path, on_left_click, on_right_click):
        self.original_image_off = pygame.image.load(image_off_path).convert_alpha()
        self.original_image_on = pygame.image.load(image_on_path).convert_alpha()

        # Set the initial size of the button
        self.size = self.original_image_off.get_size()
        self.image_off = pygame.transform.scale(self.original_image_off, self.size)
        self.image_on = pygame.transform.scale(self.original_image_on, self.size)

        self.on_left_click = on_left_click
        self.on_right_click = on_right_click

        self.click_state = False
        self.hovered_state = False
        
        self.rect = self.image_off.get_rect(center=position)

        self.button_tweens = []
        self.button_tweens_out = []

    def on_hover_enter(self):
        self.scale(1.1)    
    
    def on_hover_exit(self):
        self.scale(0.9)  

    
    def scale(self, scale_factor):
        # Calculate the new dimensions based on the original size
        new_size = int(self.original_image_off.get_width() * scale_factor), int(self.original_image_off.get_height() *  scale_factor)
        
        tween_size_data = TweenDataVector2(self.size, new_size, .5, 0, pytweening.easeOutElastic)
        self.tween_size = TweenVector2(tween_size_data) 
        self.button_tweens.append(self.tween_size)
        self.tween_size.start()
        
        # Update the button size
        self.size = self.tween_size.get_output()

        # Update the images based on the new size

    def handle_event(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.hovered_state == False:
                self.hovered_state = True
                self.on_hover_enter()
            else:
                pass       
        else:
            if self.hovered_state == True:
                self.hovered_state = False
                self.on_hover_exit()
            else:
                pass
    
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right Click
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.click_state = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            if self.click_state == True:
                self.click_state = False
                self.on_right_click()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left Click
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.click_state = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.click_state == True:
                self.click_state = False
                self.on_left_click()

    def draw(self, screen, position):
        for tween in self.button_tweens:
            tween.update()

            if tween.check_finished():
                self.button_tweens.pop(self.button_tweens.index(tween))
            else:
                self.image_off = pygame.transform.scale(self.original_image_off, self.tween_size.get_output())
                self.image_on = pygame.transform.scale(self.original_image_on, self.tween_size.get_output())

        if position == None:
            image = self.image_on if self.click_state == True else self.image_off
            screen.blit(image, self.rect)
        else:
            self.rect = self.image_off.get_rect(center=position)
            
            image = self.image_on if self.click_state == True else self.image_off
            screen.blit(image, self.rect)
