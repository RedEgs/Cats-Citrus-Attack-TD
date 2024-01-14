import pytweening, pygame, sys, os


class GuiService():
    hovered_buttons = []
    ui_elements = []

    @classmethod    
    def add_element(cls, element):
        cls.ui_elements.append(element)
       
    @classmethod 
    def draw(cls, screen):
        for element in cls.ui_elements:
            element.draw(screen)

class Element:
    def __init__(self, position, image_path):
        self.position = position
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=position)

        GuiService.add_element(self)



    def draw(self, screen):
        screen.blit(self.image, self.rect)