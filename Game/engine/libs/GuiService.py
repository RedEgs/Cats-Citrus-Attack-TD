import pytweening, pygame, sys, os
from enum import Enum

import engine.libs.Utils as utils
import engine.libs.TweenService as TweenService


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
        
        cls.ui_elements[key] = {"element": memory_location , "scene": cls.active_scene, "is_exception": element.get_element_exception()}
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
        if cls.active_scene.cached == False:
            for key, element in cls.ui_elements.items():
                obj = element["element"]
                obj_scene = element["scene"]
                obj_exception = element["is_exception"]
                
                #try:
                    #if obj_exception == True:
                        #obj.draw(screen)
                        #obj.update        
               #except AttributeError:
                    #pass            

                if cls.active_scene == obj_scene:
                    if cls.active_scene.cached == False:
                        cls.cache(obj)
                else:
                    pass

            cls.active_scene.cached = True
        else:
            for element in cls.active_scene.element_cache:
                #print("Drawing from cache")
                element.draw(screen)
                element.update()   
            
    @classmethod 
    def handle_event(cls, event):
        if cls.active_scene.cached_button == False:
            for key, element in cls.button_elements.items():
                obj = element["button_element"]
                obj_scene = element["scene"]

                
                if cls.active_scene == obj_scene:
                    if cls.active_scene.cached_button == False:
                        cls.cache_button(obj)   
                else:
                    pass

            cls.active_scene.cached_button = True

        else:
            for element in cls.active_scene.button_cache:
                element.handle_event(event)

        
    @classmethod
    def set_active_scene(cls, scene):
        cls.active_scene = scene

    @classmethod
    def cache(cls, object):
        element_cache = cls.active_scene.element_cache
        element_cache.append(object)

    @classmethod
    def cache_button(cls, object):
        button_cache = cls.active_scene.button_cache
        button_cache.append(object)


class Element:
    def __init__(self, position):
        self.position = position
        self.is_exception = False
        #self.rect = self.image.get_rect(center=position)

        GuiService.add_element(self)

    def update_position(self, position):
        self.position = position

    def update(self):
        pass

    def draw(self, screen):
        pass

    def get_element_data(self):
        return self
    
    def get_element_exception(self):
        return False

class ImageElement(Element):
    def __init__(self, position, image_path, target_size=None):
        super().__init__(position)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.size = self.image.get_size()
        aspect_ratio = self.size[0] / self.size[1]
        
        if target_size:
            self.image = utils.scale_image(self.image, target_size[0], target_size[1], aspect_ratio) 
        self.rect = self.image.get_rect(center=position)

    def update_opacity(self, opacity):
        self.image.set_alpha(opacity)

    def update_position(self, position):
        super().update_position(position)
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
       
    def get_element_data(self):
        return self
    
class SurfaceElement(Element):
    def __init__(self, position, surface, target_size=None):
        super().__init__(position)
        self.surface = surface
        self.size = self.surface.get_size()
        aspect_ratio = self.size[0] / self.size[1]
        
        if target_size:
            self.surface = utils.scale_surface(self.surface, target_size[0], target_size[1], aspect_ratio) 
        self.rect = self.surface.get_rect(center=position)

    def update_opacity(self, opacity):
        self.surface.set_alpha(opacity)

    def update_position(self, position):
        super().update_position(position)
        self.rect = self.surface.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
       
    def get_element_data(self):
        return self



class TextElement(Element):
    def __init__(self, position, text, size, color):
        super().__init__(position)
        self.text = text
        self.size = size
        self.color = color

        self.default_font = pygame.font.Font("font.ttf", size)
        self.image = self.default_font.render(self.text, True, self.color)

        GuiService.add_element(self)

    def update_position(self, position):
        super().update_position(position)
        self.rect = self.image.get_rect(center=position)

    def update_text(self, text):
        self.text = text

    def draw(self, screen):
        self.rect = self.image.get_rect(center=self.position)
        screen.blit(self.image, self.rect)
         

class ButtonState(Enum):
    DEFAULT = "default"
    DOWN = "down"
    HOVERED = "hovered" 
    DISABLED = "disabled"


class ButtonElement(Element):
    def __init__(self, position, image_pair, function_pair, ):
        super().__init__(position)
        GuiService.add_button_element(self)

        self.original_image_default = pygame.image.load(image_pair[0]).convert_alpha()
        
        try:
            self.original_image_activated = pygame.image.load(image_pair[1]).convert_alpha()
        except IndexError:
            self.original_image_activated = pygame.image.load(image_pair[0]).convert_alpha()
            

        self.function_pair = function_pair

        # Set the initial size of the 
        self.active_size_tween = None
        self.active_rotation_tween = None

        self.new_rotation = 0

        self.size = self.original_image_default.get_size()
        self.new_size = 1

        self.image_default = pygame.transform.scale(self.original_image_default, self.size)
        self.image_activated = pygame.transform.scale(self.original_image_activated, self.size)

        self.rect = self.image_default.get_rect(center=position)
        self.state = ButtonState.DEFAULT

    def update_position(self, position):
        super().update_position(position)
        self.rect = self.original_image_default.get_rect(center=position)

    def update_size(self, size):
        return utils.scale_image(self.original_image_default, size)
    
    def update_rotation(self, rotation, image):
        return utils.rotate_image(image, rotation)
     
    def rotation_animate(self, new_rotation):
        current_rotation = self.new_rotation
        
        tween_data = TweenService.TweenData(current_rotation, new_rotation, .3, 0, pytweening.easeOutExpo)
        self.active_rotation_tween = TweenService.Tween(tween_data)
        self.active_rotation_tween.start()

    def size_animate(self, new_size):
        current_size = self.new_size
        
        tween_data = TweenService.TweenData(current_size, new_size, .3, 0, pytweening.easeOutExpo)
        self.active_size_tween = TweenService.Tween(tween_data)
        self.active_size_tween.start()

    def update(self):
        image_default_s = self.update_size(self.new_size)
        self.image_default = self.update_rotation(self.new_rotation, image_default_s)

        #self.image_default_s = self.update_size(self.new_size)
        #self.image_default_s = self.update_rotation(self.new_rotation)
    
        if self.active_size_tween:
            self.new_size = self.active_size_tween.get_output()
        if self.active_rotation_tween:
            self.new_rotation = self.active_rotation_tween.get_output()

    def on_hover_enter(self):
        self.state = ButtonState.HOVERED
        self.size_animate(1.08)
        self.rotation_animate(-3)

    def on_hover_exit(self):
        self.state = ButtonState.DEFAULT
        self.size_animate(1.0)
        self.rotation_animate(0)

    def on_left_click(self):    
        self.state = ButtonState.DEFAULT
        self.function_pair[0]()

    def on_right_click(self):
        self.state = ButtonState.DEFAULT
        self.function_pair[1]()

    def handle_event(self, event):

        # Checks if the the button is hoverable
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.state == ButtonState.DEFAULT:
                self.on_hover_enter()
            else:
                pass       
        elif self.state == ButtonState.HOVERED:
                self.on_hover_exit()
        else:
            pass
    

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right Click
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.state = ButtonState.DOWN                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            if self.state == ButtonState.DOWN:
                self.on_right_click()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left Click
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.state = ButtonState.DOWN     
                if self.new_rotation != 0 or self.new_size != 1:
                    self.size_animate(1.15)
                    #self.rotation_animate(3)
                
                 
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.state == ButtonState.DOWN:
                self.on_left_click()
                self.size_animate(1)
                self.rotation_animate(0)

    def draw(self, screen):
        self.rect = self.image_default.get_rect(center=self.position)
        
        if self.image_activated and self.image_default:
            image = self.image_activated if self.state == ButtonState.DOWN else self.image_default
        elif self.image_default:
            self.image_default
            
        screen.blit(self.image_default, self.rect)
        
        











        
        



"""
class ButtonElement(Element):
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
"""