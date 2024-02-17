import pytweening, pygame, time, sys, os
import numba
from enum import Enum

import engine.libs.Utils as utils
import engine.libs.TweenService as TweenService
import engine.libs.CameraService as CameraService


class GuiServiceState(Enum):
    DRAWING = "drawing"
    LOADING = "loading"
    CACHING = "caching"


class GuiSpaces(Enum):
    WORLD = "world" 
    SCREEN = "screen"  

    # Screen space elements are rendered relative to its position on the window
    # They are rendered directly onto the screen rather than to the camera.
    
    # Global space elements behave similarly to screen space elements except they don't have the properties of normal elements.
    # To elaborate, global space elements don't contain an origin, or an index.
    # Where as normal elements are rendered based on their index, type and scene.
    # Visually they look no different to screen space elements
    
    # World space elements are rendered relative to its position on the camera, meaning if the camera move, its position on the window moves aswell
    # It is direclty influenced by the camera. Elements rendered to the camera have a world position
    
    # To compare world space elements and screen space elements; 
    # If i were to move the camera, a world space element would move with the camera, so its "global position" or "screen position" (they are synonymous) would change, although its "world position" would remain the same
    # If i were to move the camera, a screen space element would stay in the exact same place regardless of what the camera is doing. 



class ElementTypes(Enum): # Used for indicating an elements type (mainly used for ordering purposes)
    RAW = "raw" 
    ELEMENT = "element"
    EVENT = "event"


class GuiService():
    active_scene = None
    active_camera = None

    ui_elements = [] # Contains EVERY gui element
    screen_ui_elements = pygame.sprite.Group()
    screen_ui_event_elements = []
    
    global_ui_elements = pygame.sprite.Group()
    global_ui_event_elements = []
    
    @classmethod
    def add_element(cls, element):
        if cls.active_scene:
            cls.ui_elements.append(element)
            current_element_index = len(cls.ui_elements) # Gets the current length of the list for indexing purposes
            element.set_element_index(current_element_index) # Sets the elements index
            element.origin = cls.active_scene # Sets the origin of the scene
            
            if element.space == GuiSpaces.SCREEN:  # Checks which space 
                print(f"{element} is screen space")
                cls.screen_ui_elements.add(element)
                
            else:
                print(f"{element} is world space")
                cls.active_scene.ui_elements.add(element)

            print(f"Adding {element} at index {current_element_index} to {cls.active_scene.ui_elements}")
        else:
            print(f"No active scene found, adding {element} to global elements")
            cls.global_ui_elements.add(element)

    @classmethod
    def set_active_scene(cls, scene):
        cls.active_scene = scene

    @classmethod
    def load_scene_elements(cls):
        if cls.active_scene: # Makes sure that there is an active scene otherwise there is a problem
            a_s = cls.active_scene
            
            for element in cls.ui_elements: # Iterates through every single gui element 
                if element.origin == a_s: # Checks to see which scene they are from

                    if element.element_type == ElementTypes.EVENT:
                        a_s.ui_event_elements.append(element)
                        print(f"Added {element} to {a_s.ui_event_elements} with {len(a_s.ui_event_elements)} elements")
        else:
            print("No active scene found during loading phase") 
                
    
    @classmethod
    def remove_element(cls, element):
        """
        Destroys an elements sprite. Essentially deleting it from being handled or drawn
        There is no way to get a deleted element back directly
        """
        element.kill()
        
    @classmethod
    def draw(cls, camera):
        display = camera.get_display()
        screen = camera.get_screen()
        camera.guis = cls
        """
        All relevant elements are drawn at this part
        """
        
        ## Draw order of elements (top to bottom)
        # Global Elements
        # Screen Space Elements
        # World Elements
        
        
        # World Space Elements are draw under this section
       
        for element in cls.active_scene.ui_elements.sprites():        
            element.draw(display)
            element.update()

            
        # cls.active_scene.ui_elements.draw(display) 
        # cls.active_scene.ui_elements.update()
        
        

        
    
        

    @classmethod
    def handle_event(cls, event, camera: CameraService.Camera):
        """
        All relevant event elements have their events handled here
        """
 
        for element in cls.active_scene.ui_event_elements:
            element.handle_event(event)
            
        for element in cls.screen_ui_event_elements:
            element.handle_event(event)
            
        for element in cls.global_ui_event_elements:
            element.handle_event(event)
            
        if event.type == camera.camera_event:
            for element in cls.active_scene.ui_elements.sprites():
                element.update_element()
                element.update_position()


class WindowToast:
    # win10toast docs
    def __init__(self, title, body, duration, icon_path, threaded: bool):
        from win10toast import ToastNotifier

        toast = ToastNotifier()
        toast.show_toast(
            title,
            body,
            duration=duration,
            icon_path=icon_path,
            threaded=threaded,
        )


class RawElement(pygame.sprite.Sprite):
    def __init__(
        self, space: Enum = GuiSpaces.WORLD, camera: CameraService.Camera = any
    ):
        pygame.sprite.Sprite.__init__(self)  # Inherits from pygames sprites
        self.element_type = ElementTypes.RAW
        self.origin = None # This is the scene in which the element was instanced from
        # self.origin_index = 0  # May be implemented later : The index of the instance relative to all the other gui elements with the same origin scene

        self.element_index = 0  # The index in which it was instanced | E.G Index = 5 would mean it was the 5th element to be instanced
        self.camera = camera  # Contains reference to the camera
        self.space = space  # Contains the type of space in which it should be drawn in.

        GuiService.add_element(
            self
        )  # Officially makes it a GUI Element to be handle by GUI Service

    def update_element(self):
        """
        Put all code that updates any rects or positions etc.
        This is so that when a camera event is fired, the current element
        is updated on screen aswell, rather than just the position updating.
        """
        pass

    def update(self):
        """
        This is ran every tick every draw frame.
        """
        pass


    def draw(self, screen):
        """
        Everything here is for drawing your gui element to the screen
        """
        pass

    def destroy(self):
        """
        Deletes the instance of the GUI element and stops it from being rendered or updated
        """

        GuiService.uncache(self)

    def set_element_index(self, index):
        """
        Ignore if you are only making a GUI element
        To set element index from the GUI Service "draw()" function
        """

        self.element_index = index
        # print(self.element_index)


class Element(RawElement):
    def __init__(
        self,
        space: Enum = GuiSpaces.WORLD,
        camera: CameraService.Camera = any,
        position: pygame.math.Vector2 = (0,0),  # The position on screen in which the element should be instanced at
    ):
        super().__init__(space, camera)
        self.element_type = ElementTypes.ELEMENT
        self.ORIGINAL_POSITION = position  # The position in which the element was instanced at. Should be constant.

        self.screen_position = self.ORIGINAL_POSITION
        self.world_position = None
        
        if self.space == GuiSpaces.WORLD:  # This is to make sure that positioning of elements is correct for their type of space
            self.world_position = self.world_position = (self.ORIGINAL_POSITION[0] - self.camera.camera_bounds_rect.center[0], 
                                        self.ORIGINAL_POSITION[1] - self.camera.camera_bounds_rect.center[1])
            
            self.position = self.ORIGINAL_POSITION - self.camera.camera_offset  # Makes sure that elements are effected by the camera
        elif self.space == GuiSpaces.SCREEN:
            self.position = position


    def update_position(self):
        """
        This updates the position of elements for those that are using world space so that they are always affected by the camera
        Otherwise this function doesn't have much use for screen space functions.  
        """
        
 
      


        if self.space == GuiSpaces.WORLD:  # This is to make sure that positioning of elements is correct for world space
            self.world_position = (self.ORIGINAL_POSITION[0] - self.camera.camera_bounds_rect.center[0], 
                                self.ORIGINAL_POSITION[1] - self.camera.camera_bounds_rect.center[1])
            
            
            
            self.position = self.ORIGINAL_POSITION - self.camera.camera_offset  # Makes sure that elements are effected by the camera
        else: self.position = self.position
        
        self.screen_position = self.position
        
    def update_element(self):
        super().update_element()    
      
    def update(self):
        super().update() 
        
    def destroy(self):
        super().destroy()

    def set_element_index(self, index):
        super().set_element_index(index)
        
    def get_world_position(self):
        return self.world_position
    
    def get_screen_position(self):
        return self.screen_position



class EventElement(Element):
    def __init__(
        self,
        space: Enum = GuiSpaces.WORLD,
        camera: CameraService.Camera = any,
        position: pygame.math.Vector2 = (0,0), 
    ):
        super().__init__(space, camera, position)
        self.element_type = ElementTypes.EVENT

        if self.space == GuiSpaces.WORLD:
            self.mouse_pos = (pygame.mouse.get_pos()[0]/self.camera.camera_zoom_scale, 
                            pygame.mouse.get_pos()[1]/self.camera.camera_zoom_scale)  # Used so world space elements collision
        else:
            self.mouse_pos = pygame.mouse.get_pos() # Make sure to use this instead of "pygame.mouse.get_pos()" (Mainly for convention)


        self.event_element_index = None # Similar to Element indexes but specific for event elements
        self.has_focus = False

    def handle_event(self, event):
        """
        Makes sure the event elements can interface with pygames event queue. Ran time any event is fired.
        """
    def update_position(self):
        super().update_position()
        
    def update_element(self):
        super().update_element()    

    def update(self):
        super().update()
                
        if self.space == GuiSpaces.WORLD:
            self.mouse_pos = (pygame.mouse.get_pos()[0]/self.camera.camera_zoom_scale, 
                              pygame.mouse.get_pos()[1]/self.camera.camera_zoom_scale)   # Used so world space elements collision
        else:
            self.mouse_pos = pygame.mouse.get_pos() # Make sure to use this instead of "pygame.mouse.get_pos()" (Mainly for convention)

    def destroy(self):
        super().destroy()

    def set_element_index(self, index):
        super().set_element_index(index)




class ImageElement(Element):
    """
    Renders and Image on screen
    """
    def __init__(self, space, camera, position, image_path):
        super().__init__(space, camera, position)
        self.image_path = image_path # The path of the image

        self.image = pygame.image.load(image_path).convert_alpha()
        self.size = self.image.get_size()

        self.rect = self.image.get_rect(center=self.position)

    def update_image(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.size = self.image.get_size()
        
        self.rect = self.image.get_rect(center=self.position)

    def update_position(self):
        super().update_position()

    def update_element(self):
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        pass
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        

class TextElement(Element):
    def __init__(self, space, camera, position, text:str ="Placeholder", size: int=16, color: pygame.Color = (0,0,0), text_align: str ="center", underline: bool=False):
        super().__init__(space, camera, position)
        self.text = text
        self.size = size
        self.color = color
        self.text_align = text_align

        self.default_font = pygame.font.Font("font.ttf", self.size)
        self.default_font.set_underline(underline)
        
        
        self.image = self.default_font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()

        if self.text_align == "right":
            self.rect.midright = (self.position[0]-self.rect.width, self.position[1])
        if self.text_align == "center":
            self.rect.center = self.position
        if self.text_align == "left":
            self.rect.midleft = self.position
            
        
    def update_text(self, text=None):
        if text == None:
            self.image = self.default_font.render(self.text, True, self.color)
        else:
            self.text = text
            self.image = self.default_font.render(self.text, True, self.color)
            
        self.update_element()

    def update_position(self):
        super().update_position()

    def update_element(self):
        self.image = self.default_font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()

        if self.text_align == "right":
           self.rect.midright = self.position#(self.position[0]-self.rect.width, self.position[1])
        if self.text_align == "center":
            self.rect.center = self.position
        if self.text_align == "left":
            self.rect.midleft = self.position
        
    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (180, 0, 255), self.rect)
        #pygame.draw.circle(screen, (0,180,255), (self.rect.center), radius=5) # Shows align positions

class TextInput(EventElement):
    def __init__(
        self,
        space,
        camera,
        position,
        font_size: int = 24,
        init_text: str = "",
        image_path: str = None,
        text_color=(0, 0, 0),
        cursor_color=(0, 0, 0),
    ):
        super().__init__(space, camera, position)
        self.font_size = font_size
        self.text_color = text_color
        self.cursor_color = cursor_color

        if image_path:
            self.background = ImageElement(self.position, image_path, None)
        else:
            self.background = pygame.Surface((150, 50))
            self.background.fill((18, 18, 18))

        self.background_rect = self.background.get_rect(center=self.position)

        self.first_time = True

        self.init_text = init_text
        self.text = init_text
        self.display_text = self.text
        self.submitted_text = ""

        self.font = pygame.font.Font("font.ttf", self.font_size)
        self.font_image = self.font.render(self.display_text, True, self.text_color)

        self.font_image_rect = self.font_image.get_rect(center=self.position)

        self.cursor_rect = pygame.Rect(
            self.font_image.get_rect(
                center=(self.position[0] + 5, self.position[1])
            ).topright,
            (2, self.font_size),
        )
        self.unfocused_alpha = 80

    def update_position(self):
        return super().update_position()
    
    def update_element(self):
        self.background_rect = self.background.get_rect(center=self.position)
        self.font_image = self.font.render(self.text, True, self.text_color)

        self.font_image_rect = self.font_image.get_rect(center=self.position)

        self.cursor_rect = pygame.Rect(
            self.font_image.get_rect(
                center=(self.position[0] + 5, self.position[1])
            ).topright,
            (2, self.font_size),
        )
        
    def update(self):
        super().update()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left Click
            if self.background_rect.collidepoint(self.mouse_pos):
                self.has_focus = True

                if not self.first_time:
                    self.font_image.set_alpha(255)

            elif self.has_focus:
                self.has_focus = False

                if self.text == "":
                    self.text = self.init_text
                    self.first_time = True
                    self.update_element() ## change

        if event.type == pygame.KEYDOWN and self.has_focus:
            if self.first_time:
                self.text = ""
                self.first_time = False

            if event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0:
                    self.text = self.text[:-1]

            elif event.key == pygame.K_RETURN:
                self.submitted_text = self.text

            else:
                self.text += event.unicode

            self.update_element() ## change
        

    def draw(self, screen):
        if not self.has_focus:
            self.font_image.set_alpha(self.unfocused_alpha)
            
        screen.blit(self.font_image, self.font_image_rect)

        if time.time() % 1 > 0.5 and self.has_focus:
            cursor_surface = pygame.Surface((2, self.font_size), pygame.SRCALPHA)
            cursor_surface.fill((*self.cursor_color, self.unfocused_alpha))
            screen.blit(cursor_surface, self.cursor_rect.topleft)

    def get_submitted_text(self):
        self.submitted_text = self.text
        return self.submitted_text


class DraggableRect(EventElement):
    def __init__(self, space, camera, position, color, size):
        super().__init__(space, camera, position)
        self.color = color
        self.size = size
        self.resizable = False

        self.resizing_rect = False
        self.dragging_rect = False

        self.can_change_mouse = True

        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        
        self.rect = self.surface.get_rect(center=self.position)


    def update_dragged_position(self):
        self.position = self.rect.center
        
        if self.space == GuiSpaces.WORLD:
            self.ORIGINAL_POSITION = self.rect.center + self.camera.get_camera_offset()

    def update_position(self):
        super().update_position()
      
    def update_element(self):
        self.rect = self.surface.get_rect(center=self.position)

    def update(self):
        super().update()
        #print(self.rect)


    def handle_event(self, event):
        # sourcery skip: merge-nested-ifs
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(self.mouse_pos):  # Dragging Header
                self.dragging_rect = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging_rect = False

        if self.dragging_rect:
            if event.type == pygame.MOUSEMOTION:
                self.rect.move_ip(event.rel)
                self.update_dragged_position()
                self.update_position()
                

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
        
    def set_pos(self, position):
        self.rect.center = position
    
    def get_pos(self):
        return self.rect.center


class DraggableImage(DraggableRect):
    def __init__(self, space, position, size, image_path):
        super().__init__(space, position, None, size)

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.gaussian_blur(self.image, 5)

        self.size = size
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        # self.rect = pygame.Rect(self.position, self.size)
        self.resizable = False

        self.resizing_rect = False
        self.dragging_rect = False

    def handle_event(self, event, offset_pos):
        super().handle_event(event)

    def draw(self, screen, offset_pos):

        screen.blit(self.image, offset_pos)


class StatusBar(Element):  # Image Support
    def __init__(
        self,
        space,
        camera,
        position,
        size,
        color=(255, 0, 0),
        range_value=(0, 100),
        initial_value=1,
    ):
        super().__init__(space, camera, position)
        self.size = size
        self.color = color
        self.range_value = range_value
        self.initial_value = initial_value

        self.bar_left_pos = self.position[0]
        self.bar_right_pos = self.position[0] + self.size[0]
        self.bar_center_pos = self.bar_right_pos - self.bar_left_pos

        self.value_ratio = self.range_value[1] / self.size[0]
        
        self.bar_background = pygame.Surface(self.size)
        self.bar_background.fill((140, 140, 140))
        
        self.bar_fill = pygame.Surface((initial_value / self.value_ratio, self.size[1]))
        self.bar_fill.fill(self.color)
        
        self.bar_background_rect = self.bar_background.get_rect(center=self.position)
        self.bar_fill_rect = self.bar_fill.get_rect(midleft=self.bar_background_rect.midleft)
        
        print(self.bar_background, self.bar_fill)
        print(self.bar_background_rect, self.bar_fill_rect)

    def set_value(self, percentage):
        self.bar_left_pos = self.position[0]
        self.bar_right_pos = self.position[0] + self.size[0]
        self.bar_center_pos = self.bar_right_pos - self.bar_left_pos

        self.value_ratio = self.range_value[1] / self.size[0]
        
        self.bar_fill = pygame.Surface((percentage / self.value_ratio, self.size[1]))
        self.bar_fill.fill(self.color)

    def get_value(self):
        return self.bar_fill_rect.width / (self.value_ratio * (self.size[0] / 100) ** 2)

    def update_position(self):
        super().update_position()


    def update_element(self):
        self.bar_left_pos = self.position[0]
        self.bar_right_pos = self.position[0] + self.size[0]
        self.bar_center_pos = self.bar_right_pos - self.bar_left_pos

        self.value_ratio = self.range_value[1] / self.size[0]
        
        self.bar_background_rect = self.bar_background.get_rect(center=self.position)
        self.bar_fill_rect = self.bar_fill.get_rect(midleft=self.bar_background_rect.midleft)
        
    def update(self):
        pass

    def draw(self, screen):
        
        screen.blit(self.bar_background, self.bar_background_rect)
        screen.blit(self.bar_fill, self.bar_fill_rect)        


class Slider(EventElement):  # Finish with images etc
    def __init__(
        self,
        space,
        camera,
        position,
        size=(200, 300),
        range_value=(0, 100),
        initial_value:int =None,
    ):
        super().__init__(space, camera, position)
        self.size = size
        self.range_value = range_value

        self.dragging_rect = False

        self.slider_left_pos = self.position[0]
        self.slider_right_pos = self.position[0] + self.size[0]
        self.slider_center_pos = self.slider_right_pos - self.slider_left_pos


        self.background = pygame.Surface(self.size)
        self.background.fill((220, 0, 0))
        
        self.sliding_point = pygame.Surface((self.size[0] // 15, self.size[1] * 1.3))
        self.sliding_point.fill((0, 255, 0))

        self.background_rect = self.background.get_rect(center=self.position)
        self.sliding_point_rect = self.sliding_point.get_rect(center=self.position)
       
        self.slider_position = self.sliding_point_rect.center
        self.previous_slider_position = self.slider_position
        
        # if initial_value is None:
        #     self.sliding_point_rect.center = self.position
        # else:
        #     self.initial_value = (self.slider_right_pos - self.slider_left_pos) * initial_value
        #     self.sliding_point_rect.center = ((self.slider_left_pos + (initial_value / range_value[1] * 100)), self.position[1])



    def get_value(self):
        value_range = self.slider_right_pos - self.slider_left_pos
        slide_range = self.sliding_point_rect.centerx - self.slider_left_pos

        return (slide_range / value_range) * (
            self.range_value[1] - self.range_value[0]
        ) + self.range_value[0]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.sliding_point_rect.collidepoint(self.mouse_pos):
                self.dragging_rect = True

            if self.background_rect.collidepoint(self.mouse_pos):
                self.sliding_point_rect.centerx = self.mouse_pos[0]
                self.slider_position = self.sliding_point_rect.center + self.camera.get_camera_offset()
                self.has_focus = True

            else:
                self.has_focus = False

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging_rect = False

        # sourcery skip: merge-nested-ifsz
        if self.dragging_rect:
            if (
                event.type == pygame.MOUSEMOTION
            ):  # Controls the movement of the WHOLE window
                if self.background_rect.collidepoint(self.mouse_pos):
                    self.sliding_point_rect.centerx = self.mouse_pos[0]
                    self.slider_position = self.sliding_point_rect.center + self.camera.get_camera_offset()
                    
                    
        # sourcery skip: merge-nested-ifs
        if self.has_focus and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not self.sliding_point_rect.centerx <= self.slider_left_pos:
                    self.sliding_point_rect.centerx -= 1
            if event.key == pygame.K_RIGHT:
                if not self.sliding_point_rect.centerx >= self.slider_right_pos:
                    self.sliding_point_rect.centerx += 1

    def update_position(self):
        super().update_position()

    def update_element(self):
        self.previous_slider_position = self.slider_position - self.camera.get_camera_offset()
        
        self.slider_left_pos = self.position[0]
        self.slider_right_pos = self.position[0] + self.size[0]
        self.slider_center_pos = self.slider_right_pos - self.slider_left_pos

        self.background_rect = self.background.get_rect(center=self.position)
        self.sliding_point_rect = self.sliding_point.get_rect(center=self.previous_slider_position)


    def update(self):
        super().update()

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0,0), self.mouse_pos, 10)
        screen.blit(self.background, self.background_rect)
        screen.blit(self.sliding_point, self.sliding_point_rect)


class Checkbox(EventElement):  # Add image loading
    def __init__(self, space, camera, position, size=(20, 20), toggled=False):
        super().__init__(space, camera, position)
        self.size = size
        
        
        self.background = pygame.Surface(self.size)
        self.background.fill((0,255,0))

        self.fill = pygame.Surface( (self.size[0] * 0.6, self.size[0] * 0.6))
        self.fill.fill((255, 0, 0))
    
        self.background_rect = self.background.get_rect(center=self.position)
        self.fill_rect = self.fill.get_rect(center=self.background_rect.center)

        self.toggled = toggled

    def update_element(self):
        super().update_element()
        
        self.background_rect = self.background.get_rect(center=self.position)
        self.fill_rect = self.fill.get_rect(center=self.background_rect.center)

    def update_position(self):
        return super().update_position()
    
    def update(self):
        super().update()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.background_rect.collidepoint(self.mouse_pos):
                self.toggled = not self.toggled

    def draw(self, screen):
        screen.blit(self.background, self.background_rect)

        if self.toggled:
            screen.blit(self.fill, self.fill_rect)

class EasyCurve(RawElement):
    def __init__(
        self, space, camera, point1, point2, line_color=(255, 0, 255), line_thickness=10
    ):
        super().__init__(space, camera)
        from pygame import gfxdraw

        self.point1 = point1
        self.point2 = point2

        if self.space == GuiSpaces.WORLD:
            self.start = point1 - self.camera.get_camera_offset()
            self.end = point2 - self.camera.get_camera_offset()
        else:
            self.start = point1 
            self.end = point2
            
            
        self.line_color = line_color
        self.line_thickness = line_thickness

        if self.space == GuiSpaces.WORLD:
            dist_1 = self.midpoint(self.start, self.end) + self.camera.get_camera_offset()
            dist_2 = self.midpoint(self.end, self.start) + self.camera.get_camera_offset()
        else:
            dist_1 = self.midpoint(self.start, self.end) 
            dist_2 = self.midpoint(self.end, self.start)

        self.middle_1 = (self.start[0] + dist_1[0], self.start[1])
        self.middle_2 = (self.end[0] - dist_2[0], self.end[1])

    def distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2

        z1 = x2 - x1
        z2 = y2 - y1

        return (z1, z2)

    def midpoint(self, point1, point2):
        """Calculate the midpoint of a segment defined by two points."""
        x1, y1 = point1
        x2, y2 = point2
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        return (mid_x, mid_y)

    def set_points(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

        if self.space == GuiSpaces.WORLD:
            self.start = point1 - self.camera.get_camera_offset()
            self.end = point2 - self.camera.get_camera_offset()
        else:
            self.start = point1 
            self.end = point2
            
        if self.space == GuiSpaces.WORLD:
            dist_1 = self.midpoint(self.start, self.end) + self.camera.get_camera_offset()
            dist_2 = self.midpoint(self.end, self.start) + self.camera.get_camera_offset()
        else:
            dist_1 = self.midpoint(self.start, self.end) 
            dist_2 = self.midpoint(self.end, self.start)

        self.middle_1 = (self.start[0] + dist_1[0], self.start[1])
        self.middle_2 = (self.end[0] - dist_2[0], self.end[1])
        
    def update_position(self):
        pass
    
    def update_element(self):
        self.set_points(self.point1, self.point2)
    
    def draw(self, screen):
        from pygame import gfxdraw

        gfxdraw.bezier(
            screen,
            (self.start, self.middle_1, self.middle_2, self.end),
            self.line_thickness,
            self.line_color,
        )


class ButtonState(Enum):
    DEFAULT = "default"
    DOWN = "down"
    HOVERED = "hovered"
    DISABLED = "disabled"


class ButtonElement(EventElement):
    def __init__(
        self,
        space,
        camera,
        position: pygame.Vector2,
        image_pair: list = None,
        function_pair: list = None,
        hover_function_pair: list = None,
        size_animation=True,
        rotation_animation=True,
        button_text: str = None,
    ):  # sourcery skip: hoist-statement-from-if  # sourcery skip: hoist-statement-from-if
        super().__init__(space, camera, position)

        if image_pair:
            self.original_image_default = pygame.image.load(
                image_pair[0]
            ).convert_alpha()

            try:
                self.original_image_activated = pygame.image.load(
                    image_pair[1]
                ).convert_alpha()
            except IndexError:
                self.original_image_activated = pygame.image.load(
                    image_pair[0]
                ).convert_alpha()

            self.size = self.original_image_default.get_size()
            self.image_default = pygame.transform.scale(
                self.original_image_default, self.size
            )
            self.image_activated = pygame.transform.scale(
                self.original_image_activated, self.size
            )
            self.rect = self.image_default.get_rect(center=self.position)

        else:
            self.original_image_default = pygame.Surface((150, 50))
            self.original_image_activated = self.original_image_default

            self.size = self.original_image_default.get_size()
            self.image_default = pygame.transform.scale(
                self.original_image_default, self.size
            )
            self.image_activated = pygame.transform.scale(
                self.original_image_activated, self.size
            )
            self.original_image_default.fill((245, 66, 66))

            self.rect = self.image_default.get_rect(center=self.position)

        self.image_pair = image_pair
        self.function_pair = function_pair
        self.hover_function_pair = hover_function_pair

        # Set the initial size of the
        self.active_size_tween = None
        self.active_rotation_tween = None

        self.new_rotation = 0
        self.new_size = 1

        self.state = ButtonState.DEFAULT

        self.size_animation = size_animation
        self.rotation_animation = rotation_animation

    def set_position(self, position):
        self.rect = self.original_image_default.get_rect(center=position)

    def update_size(self, size):
        return utils.scale_image(self.original_image_default, size)

    def update_rotation(self, rotation, image):
        return utils.rotate_image(image, rotation)

    def rotation_animate(self, new_rotation):
        current_rotation = self.new_rotation

        tween_data = TweenService.TweenData(
            current_rotation, new_rotation, 0.3, 0, pytweening.easeOutExpo
        )
        self.active_rotation_tween = TweenService.Tween(tween_data)
        self.active_rotation_tween.start()

    def size_animate(self, new_size):
        current_size = self.new_size

        tween_data = TweenService.TweenData(
            current_size, new_size, 0.3, 0, pytweening.easeOutExpo
        )
        self.active_size_tween = TweenService.Tween(tween_data)
        self.active_size_tween.start()


    def on_hover_enter(self):
        self.state = ButtonState.HOVERED

        if self.hover_function_pair:
            self.hover_function_pair[0]

        if self.size_animation:
            self.size_animate(1.08)
        if self.rotation_animation:
            self.rotation_animate(-3)

    def on_hover_exit(self):
        self.state = ButtonState.DEFAULT

        if self.hover_function_pair:
            self.hover_function_pair[1]

        if self.size_animation:
            self.size_animate(1.0)
        if self.rotation_animation:
            self.rotation_animate(0)

    def on_left_click(self):
        self.state = ButtonState.DEFAULT
        self.function_pair[0]()

    def on_right_click(self):
        self.state = ButtonState.DEFAULT
        self.function_pair[1]()

    def update_position(self):
        return super().update_position()
    
    def update_element(self):
        self.rect = self.image_default.get_rect(center=self.position)
        
    def update(self):
        super().update()

        image_default_s = self.update_size(self.new_size)
        self.image_default = self.update_rotation(self.new_rotation, image_default_s)

        # self.image_default_s = self.update_size(self.new_size)
        # self.image_default_s = self.update_rotation(self.new_rotation)

        if self.active_size_tween:
            self.new_size = self.active_size_tween.get_output()
        if self.active_rotation_tween:
            self.new_rotation = self.active_rotation_tween.get_output()

    
    
    def handle_event(self, event):

        # Checks if the the button is hoverable
        if self.rect.collidepoint(self.mouse_pos):
            if self.state == ButtonState.DEFAULT:
                self.on_hover_enter()
        elif self.state == ButtonState.HOVERED:
            self.on_hover_exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right Click
            if self.rect.collidepoint(self.mouse_pos):
                self.state = ButtonState.DOWN
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            if self.state == ButtonState.DOWN:
                self.on_right_click()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left Click
            if self.rect.collidepoint(self.mouse_pos):
                self.state = ButtonState.DOWN
                if self.new_rotation != 0 or self.new_size != 1:
                    self.size_animate(1.15)
                    # self.rotation_animate(3)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.state == ButtonState.DOWN:
                self.on_left_click()
                self.size_animate(1)
                self.rotation_animate(0)

    def draw(self, screen):
        self.rect = self.image_default.get_rect(center=self.position)

        if self.image_activated and self.image_default:
            image = (
                self.image_activated
                if self.state == ButtonState.DOWN
                else self.image_default
            )

        screen.blit(self.image_default, self.rect)
