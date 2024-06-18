# Main project file
import pygame, sys, os
import pyredengine as pyr

import scenes.example_scene as example_scene

class MainGame(pyr.App):
    def __init__(self, override_config=False, preview_mode=True):
        super().__init__(override_config, preview_mode)

    def load_scenes(self):

        self.scene_service.load_scenes([example_scene.Example_Scene("example_scene", self)])

       
        self.scene_service.set_scene("example_scene")




# class MainGame():
#     def __init__(self, parent) -> None:
#         pygame.init()

#         self._init_display()
#         self.clock = pygame.time.Clock()
#         self.run = True
#         self.mouse_pos = (0,0) 
#         self.cont_time = 0.0
#         #HOTSAVE
        
#     def _init_display(self): # Don't touch 
#         """Initialises the display to be rendered within the viewport window of the engine"""
#         self._hwnd = None
#         if len(sys.argv) > 1:
#             self._hwnd = int(sys.argv[1])
#             os.environ['SDL_WINDOWID'] = str(self._hwnd)
        
#         self.display_width = 1280
#         self.display_height = 720
        
#         os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (-1000, -1000)
#         self.display = pygame.display.set_mode((self.display_width, self.display_height), pygame.NOFRAME)
#         pygame.display.set_caption("Pygame Window")
        
#     def _send_event(self, type, key = None, mouse_x = None, mouse_y = None):
#         """Manages event handling between viewport window and the game"""
    
#         if type == 1:
#             event = pygame.event.Event(pygame.KEYDOWN, key=key)
#             pygame.event.post(event)
#         elif type == 2:
#             last_pos = (mouse_x, mouse_y)
            
#             if last_pos:
#                 rel_x = mouse_x - last_pos[0]
#                 rel_y = mouse_y - last_pos[1]
#             else:
#                 rel_x, rel_y = 0, 0

#             last_pos = (mouse_x, mouse_y)
                        
#             event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (mouse_x, mouse_y), 'rel': (rel_x, rel_y), 'buttons': pygame.mouse.get_pressed()})
#             pygame.event.post(event)
#             pygame.mouse.set_pos(mouse_x, mouse_y)
        
#     def handle_events(self):
#         """Handles custom user events"""

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.run = False
#             if event.type == pygame.MOUSEMOTION: 
#                 self.mouse_pos = event.pos

            
#     def update(self):
#         """Put all your custom logic here"""
#         self.cont_time += 0.01
#         #print(self.cont_time)

#     def draw(self):
#         """Custom drawing logic here"""
#         import math
        
        
#         self.display.fill((255, 255, 255))
#         pygame.draw.circle(self.display, (0, 255, 0), (1280//2 + math.sin(self.cont_time) * 100, 
#                                                        720//2), 20)
        
#         pygame.display.flip()
    
#     def run_game(self):
#         """Handles the running of the game"""
        
#         while self.run: # Don't touch
#             self.clock.tick()
#             self.handle_events()
#             self.update()
#             self.draw()
            
#             yield self.display

#         pygame.quit()
#         sys.exit()
        
#     def close_game(self):
#         self.run = False
#         pygame.quit()
    
