import pytweening, pygame, sys, os
import time
from enum import Enum



import engine.libs.Utils as utils
import engine.libs.TweenService as TweenService


class GuiService():
    
    element_index = 0
    event_element_index = 0
    ui_elements = {}
    event_elements = {}
    active_scene = None


    @classmethod    
    def add_element(cls, element):
        import engine.libs.SceneService as SceneService
        
        memory_location = element.get_element_data()
        key = cls.element_index
        element.element_index = cls.element_index
        
        cls.ui_elements[key] = {"element": memory_location , "scene": cls.active_scene, "is_exception": element.get_element_exception()}
        cls.element_index += 1  # Increment the index for the next element
        
    
    @classmethod
    def add_event_element(cls, element):
        import engine.libs.SceneService as SceneService
        
        memory_location = element.get_element_data()
        key = cls.element_index
        element.event_element_index = cls.event_element_index
        
        cls.event_elements[key] = {"event_element": memory_location , "scene": cls.active_scene}
        cls.event_element_index += 1  # Increment the index for the next element
        

        
        
        
        

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
        if cls.active_scene.cached_event_element == False:
            for key, element in cls.event_elements.items():
                obj = element["event_element"]
                obj_scene = element["scene"]

                
                if cls.active_scene == obj_scene:
                    if cls.active_scene.cached_event_element == False:
                        cls.cache_event_element(obj)   
                else:
                    pass

            cls.active_scene.cached_event_element = True

        else:
            for element in cls.active_scene.event_element_cache:
                element.handle_event(event)

        
    @classmethod
    def set_active_scene(cls, scene):
        cls.active_scene = scene

    @classmethod
    def cache(cls, object):
        element_cache = cls.active_scene.element_cache
        element_cache.append(object)

    def uncache(cls, object):
        element_cache = cls.active_scene.element_cache
        element_cache.pop(object)
        
        print("uncached" + str(object))

    @classmethod
    def cache_event_element(cls, object):
        event_element_cache = cls.active_scene.event_element_cache
        event_element_cache.append(object)
        
    @classmethod
    def uncache_event_element(cls, object):
        event_element_cache = cls.active_scene.event_element_cache
        event_element_cache.pop(object)

                
    @classmethod
    def remove_element(cls, element, index):
        current_item = None
        if index in cls.ui_elements:
            current_item = cls.ui_elements[index]
            #del cls.ui_elements[index]
            
        event_element_cache = cls.active_scene.event_element_cache
        event_element_cache.append(element)
        
        event_element_cache = cls.active_scene.event_element_cache
        event_element_cache.remove(element)

  
        
        cls.active_scene.element_cache.pop(utils.is_in_list(current_item, cls.active_scene.element_cache))
        del cls.ui_elements[index]
        


class Element:
    def __init__(self, position):
        self.position = position
        self.element_index = None
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

class EventElement(Element):
    def __init__(self, position):
        super().__init__(position)
        self.event_element_index = None
        GuiService.add_event_element(self)
        

    def update_position(self, position):
        self.position = position

    def handle_event(self, event):
        pass

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
        self.position = position
        self.image_path = image_path
        self.target_size = target_size
        
        
        self.image = pygame.image.load(image_path).convert_alpha()
        self.size = self.image.get_size()
        aspect_ratio = self.size[0] / self.size[1]
        
        if target_size:
            self.image = utils.scale_image(self.image, target_size[0], target_size[1], aspect_ratio) 
        self.rect = self.image.get_rect(center=position)

    def update_image(self, image):
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.size = self.image.get_size()
        aspect_ratio = self.size[0] / self.size[1]
        
        if self.target_size:
            self.image = utils.scale_image(self.image, self.target_size[0], self.target_size[1], aspect_ratio) 
        self.rect = self.image.get_rect(center=self.position)

    def update_opacity(self, opacity):
        self.image.set_alpha(opacity)

    def update_position(self, position):
        super().update_position(position)
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
       
    def get_element_data(self):
        return self
    
    def get_rect(self, position = None):
        if position:
            return self.image.get_rect(center = position)
        else:
            return self.image.get_rect()
    
class SurfaceElement(Element):
    def __init__(self, position, surface, target_size=None):
        super().__init__(position)
        self.position = position
        self.surface = surface
        self.target_size = target_size

        self.size = self.surface.get_size()
        aspect_ratio = self.size[0] / self.size[1]
        
        if target_size:
            self.surface = utils.scale_image_by_res(self.surface, target_size[0], target_size[1], aspect_ratio) 
        self.rect = self.surface.get_rect(center=position)

    def update_surface(self, surface):
        self.surface = surface
        self.size = self.surface.get_size()
        aspect_ratio = self.size[0] / self.size[1]
        
        if self.target_size:
            self.surface = utils.scale_image_by_res(self.surface, self.target_size[0], self.target_size[1], aspect_ratio) 
        self.rect = self.surface.get_rect(center=self.position)

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

        self.default_font = pygame.font.Font("virgil.ttf", size)
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

class TextArea(EventElement):
    def __init__(self, position, init_text, image_path, text_color = (0,0,0), cursor_color = (0,0,0)):
        super().__init__(position)  
        self.position = position

        self.text_color = text_color
        self.cursor_color = cursor_color

        self.background = ImageElement(self.position, image_path, None)
        self.back_rect = self.background.get_rect(self.position)

        self.has_focus = False
        self.first_time = True

        self.text = init_text
        self.submitted_text = ""
        self.font = pygame.font.Font("virgil.ttf", 24)
        self.image = self.font.render(self.text, True, self.text_color)
        
        self.rect = self.image.get_rect(center = self.position)
        
        self.cursor_rect= pygame.Rect(self.image.get_rect(center = (self.position[0]+5, self.position[1]+4)).topright, (2, 20))
        


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left Click
            if self.back_rect.collidepoint(pygame.mouse.get_pos()):
                self.has_focus = True
                
            elif self.has_focus:
                self.has_focus = False

        
        if event.type == pygame.KEYDOWN:
            if self.has_focus:
                
                if self.first_time == True:
                    self.text = ""
                    self.first_time = False
                
                if event.key == pygame.K_BACKSPACE:
                    if len(self.text)>0:
                        self.text = self.text[:-1]
                
                elif event.key == pygame.K_RETURN:
                    self.submitted_text = self.text
                
                else:
                    self.text += event.unicode

    
                self.image = self.font.render(self.text, True, (0))
                self.rect = self.image.get_rect(center = self.position)
                self.cursor_rect = pygame.Rect(self.image.get_rect(center = (self.position[0]+5, self.position[1]+3)).topright, (2, 20))
                

    def draw(self, screen):
        if self.has_focus:
            screen.blit(self.image, self.rect)
        else:
            self.image.set_alpha(80)
            screen.blit(self.image, self.rect)
        
        if time.time() % 1 > 0.5:
            if self.has_focus:
                # Set the cursor color with alpha channel for opacity
                cursor_surface = pygame.Surface((2, 20), pygame.SRCALPHA)
                cursor_surface.fill((self.cursor_color[0], self.cursor_color[1], self.cursor_color[2], 128))  # Adjust alpha as needed
                screen.blit(cursor_surface, self.cursor_rect.topleft)

        
        
    def get_submitted_text(self):
        return self.submitted_text
class SubWindow(EventElement): # Figure out how to delete windows and elements

    def __init__(self, position, window_title, window_size, window_color = (40,40,40)):
        super().__init__(position)
        self.position = position
        self.window_size = window_size
        self.window_title = window_title
        
        self.window_color = window_color
        
        
        
        self.window_rect = pygame.Rect(self.position, self.window_size)
        
        self.header_rect = pygame.Rect((self.position[0]+10, self.position[1]), (self.window_size[0]-10, 10))
        self.resizer_rect = pygame.Rect(self.position, (10, 10))
        self.close_rect = pygame.Rect((self.position[0]+self.window_size[0]-10, self.position[1]), (10, 10))
 
        self.header_text = TextElement(self.header_rect.center, self.window_title, 8, (255,255,255))
        
        self.has_focus = False
        self.dragging_window = False
        self.resizing_window = False

    def handle_event(self, event):
        # Header
        # Resizer
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            if self.close_rect.collidepoint(pygame.mouse.get_pos()): # Dragging Header
                self.close_window()
      
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            if self.header_rect.collidepoint(pygame.mouse.get_pos()): # Dragging Header
                self.dragging_window = True
            
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1: 
            self.dragging_window = False
                
                
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            if self.resizer_rect.collidepoint(pygame.mouse.get_pos()): # Dragging Header
                self.resizing_window = True
            
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1: 
            self.resizing_window = False
                
            
        if self.dragging_window:
            if event.type == pygame.MOUSEMOTION: # Controls the movement of the WHOLE window 
                self.window_rect.move_ip(event.rel)
                
                self.header_rect.move_ip(event.rel)
                self.resizer_rect.move_ip(event.rel)
                self.close_rect.move_ip(event.rel)
        
        if self.resizing_window:
            if event.type == pygame.MOUSEMOTION:
                self.window_rect.width += event.rel[0]
                self.window_rect.height += event.rel[1]
            
                self.header_rect.width += event.rel[0]
            
                if self.window_rect.width <= 35:  # Check minimum size and position
                    self.window_rect.width = 30
                    self.header_rect.width = 20
                
                if self.window_rect.height <= 20:  # Check minimum size and position
                    self.window_rect.height = 20        
    
    def draw(self, screen):
        self.window = pygame.draw.rect(screen, self.window_color, self.window_rect)
        self.header_text.update_position(self.header_rect.center)
        pygame.draw.rect(screen, (18,18,18), self.header_rect) # Sort out tile opacity
        pygame.draw.rect(screen, (18,18,18), self.resizer_rect)
        pygame.draw.rect(screen, (255,0,0), self.close_rect)

    def close_window(self):
        GuiService.remove_element(self, self.element_index)
    

class ButtonState(Enum):
    DEFAULT = "default"
    DOWN = "down"
    HOVERED = "hovered" 
    DISABLED = "disabled"

class ButtonElement(EventElement):
    def __init__(self, position, image_pair, function_pair, ):
        super().__init__(position)
        
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