import pytweening, pygame, sys, os

class GuiService():
    
    element_index = 0
    ui_elements = {}
    button_elements = {}
    active_scene = None


    @classmethod    
    def add_element(cls, element):
        import engine.libs.SceneService as SceneService
        
        memory_location = element.get_element_data()
        key = cls.element_index
        
        cls.ui_elements[key] = {"element": memory_location , "scene": cls.active_scene}
        cls.element_index += 1  # Increment the index for the next element
    
    @classmethod
    def add_button_element(cls, element):
        import engine.libs.SceneService as SceneService
        
        memory_location = element.get_element_data()
        key = cls.element_index
        
        cls.button_elements[key] = {"button_element": memory_location , "scene": cls.active_scene}
        cls.element_index += 1  # Increment the index for the next element

    @classmethod 
    def draw(cls, screen):
        for key, element in cls.ui_elements.items():
            obj = element["element"]
            obj_scene = element["scene"]

                    
            #print(element)

            if cls.active_scene == obj_scene:
                obj.draw(screen)
            else:
                pass
            
    @classmethod 
    def handle_event(cls, event):
        for key, element in cls.button_elements.items():
            obj = element["button_element"]
            obj_scene = element["scene"]

            
            if cls.active_scene == obj_scene:
                obj.handle_event(event)
            else:
                pass
        
    @classmethod
    def set_active_scene(cls, scene):
        cls.active_scene = scene

class Element:
    
    def __init__(self, position, image_path):
        self.position = position
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=position)

        GuiService.add_element(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def get_element_data(self):
        return self

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
        
    def get_element_data(self):
        return self
        
class ButtonElement():
    def __init__(self, position, image_off_path, image_on_path, on_left_click, on_right_click): 
        self.position = position
       
        self.original_image_off = pygame.image.load(image_off_path).convert_alpha()
        self.original_image_on = pygame.image.load(image_on_path).convert_alpha()

        # Set the initial size of the button
        self.size = self.original_image_off.get_size()
        self.image_off = pygame.transform.smoothscale(self.original_image_off, self.size)
        self.image_on = pygame.transform.smoothscale(self.original_image_on, self.size)

        self.on_left_click = on_left_click
        self.on_right_click = on_right_click

        self.click_state = False
        self.hovered_state = False
        
        self.rect = self.image_off.get_rect(center=position)

        GuiService.add_element(self)
        GuiService.add_button_element(self)

    def on_hover_enter(self):
        pass

    def on_hover_exit(self):
        pass

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

    def draw(self, screen):
        self.rect = self.image_off.get_rect(center=self.position)
        
        if self.image_on and self.image_off:
            image = self.image_on if self.click_state == True else self.image_off
        elif self.image_off:
            image = self.image_off
            
        screen.blit(image, self.rect)
        
    def get_element_data(self):
        return self