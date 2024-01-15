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

class TextElement():
    def __init__(self, position, text, size, color):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.position = position
        self.text = text
        self.size = size
        self.color = color
        self.default_font = pygame.font.Font("font.ttf", size)

        self.image = self.default_font.render(self.text, True, self.color)

        GuiService.add_element(self)

    def draw(self, screen):
        self.rect = self.image.get_rect(center=self.position)

        screen.blit(self.image, self.rect)