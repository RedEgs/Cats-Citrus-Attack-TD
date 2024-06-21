# Main project file
import pygame, sys, os, random
from pyredengine import PreviewMain

class Item:
    def __init__(self, position: pygame.Vector2) -> None:
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        self.path = "gun.png"
        self.image = pygame.image.load(self.path).convert_alpha()
        self.rect = self.image.get_rect(center=position)

    def get_position(self):
        return self.rect.topleft

    def get_grid_bounds(self):
        return [self.rect.topleft, self.rect.bottomright]


    def draw(self, display: pygame.Surface):
        display.blit(self.image, self.rect)

    
class Main(PreviewMain.MainGame):
    def __init__(self) -> None:
        super().__init__()


        self.grid_size = 30
        #HOTSAVE
        
        self.draw_buffer = []
        
        self.rect_buffer = []
        
        self.current_box = None
        
        for i in range(3):
            item = Item((random.randint(0, 1280)//self.grid_size, 
                         random.randint(0, 720)//self.grid_size))
            self.draw_buffer.append(item)
            self.rect_buffer.append(item.rect)
        
    def check_box(self):
        for index, r in  enumerate(self.rect_buffer):
            if r.collidepoint(self.mouse_pos):
                return index
      
    def move_box(self, index):
        if index != None:
            self.rect_buffer[index].move_ip(self.mouse_rel)
            print("Moving")
             
    def snap_to_grid(self, pos):
        x, y = pos
        snapped_x = (x // self.grid_size) * self.grid_size
        snapped_y = (y // self.grid_size) * self.grid_size
        return (snapped_x, snapped_y)

    def draw_grid(self, display):
        width = 1280
        height = 720
        grid_color = (255, 255, 0)
        
        
        for x in range(0, width, self.grid_size):
            pygame.draw.line(display, grid_color, (x, 0), (x, height))
        for y in range(0, height, self.grid_size):
            pygame.draw.line(display, grid_color, (0, y), (width, y))
            

        
    def handle_events(self):
        #super().handle_events()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.current_box = self.check_box()
            if event.type == pygame.MOUSEMOTION:
                self.move_box(self.current_box)            
            if event.type == pygame.MOUSEBUTTONUP:
                self.rect_buffer[self.current_box].topleft = self.snap_to_grid(self.rect_buffer[self.current_box].topleft)
                self.current_box = None
            
    # def update(self):
    #     """Put all your custom logic here"""
    #     pass

    def draw(self):
        """Custom drawing logic here"""
        import math
        
        
        self.display.fill((255, 0, 0))
        for i in self.draw_buffer:
            i.draw(self.display)
        
        self.draw_grid(self.display)
        # for i in self.rect_buffer:
        #     pygame.draw.rect(self.display, (255,0,0), i)
  
        pygame.display.flip()
    
    def test_run(self):
        """Handles the running of the game"""
        
        while self.run: # Don't touch
            self.clock.tick()
            self.handle_events()
            self.update()
            self.draw()
            
            #yield self.display

        pygame.quit()
        sys.exit()
    
# m = Main()
# m.test_run()