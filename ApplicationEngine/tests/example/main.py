# Main project file
import pygame, os
from pyredengine import PreviewMain # type: ignore

"""
All code given is the bare minimum to safely run code within the engine.
Removing any code that already exists in not recommended and you WILL run into issues.
When compiled, parts of code are removed to optimise and simplify the file.
"""


class Main(PreviewMain.MainGame):
    def __init__(self, fullscreen = False) -> None:
        super().__init__(fullscreen)
        """
        Make sure not to remove the super() method above, as it will break the whole script.
        """
        self.display = pygame.display.get_surface()
        self.display_width, self.display_height = self.display.get_size()
        
        if self._engine_mode:
            abspath = os.path.abspath(__file__)
            dname = os.path.dirname(abspath)
            os.chdir(dname)
            
            
        self.centerx = self.display_width // 2
        self.centery = self.display_height // 2
            
        self.radius = 250
        self._h_angle_speed = 0.001
        self.square_size = 50
        self.square_color = pygame.Color(255, 255, 255) 

        self.pos = (0,0) 
        self._h_angle = 0 #[HOTSAVE]
        self.list = [] #[PUBLIC]
        self.flex_var = None #[PUBLIC]
        
        for i in range(5):
            self.list.append(5)
        
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.square_size, self.square_size) 

    def handle_events(self): 
        """
        All your logic for handling events should go here. 
        Its recommended you write code to do with event handling here.
        Make sure that you don't remove the `pygame.QUIT` event as the game won't be able to be shutdown.
        See pygame docs for more info: https://www.pygame.org/docs/ref/event.html.
        """
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
               
    def update(self):
        """
        This is where you independant code goes. 
        This is purely a conceptual seperator from the rest of the game code.
        Think of this as the "body" of your program.
        """
        import math
        
        self._h_pos_x = self.centerx + self.radius * math.cos(self._h_angle) - self.square_size // 2 #HOTSAVE
        self._h_pos_y = self.centery + self.radius * math.sin(self._h_angle) - self.square_size // 2 #HOTSAVE
        self.pos = (self._h_pos_x, self._h_pos_y) 
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.square_size, self.square_size)




    def draw(self):
        """
        This is where your drawing code should do.
        Make sure that `pygame.display.flip()` is the last line.
        Make sure that `self.display.fill()` is at the start too.
        
        """
        self.display.fill((180, 100, 20))
        
        
        pygame.draw.rect(self.display, self.square_color, self.rect)

        self._h_angle += self._h_angle_speed
        
        pygame.display.flip()
    
    