# Main project file
import pygame, sys, os, random
from pyredengine import PreviewMain

class Item:
    def __init__(self, position: pygame.Vector2) -> None:
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        self.path = "gun.png"
        
        self.image = pygame.transform.scale(pygame.image.load(self.path).convert_alpha(), (300, 90))
        self.d_image = pygame.transform.scale(pygame.image.load(self.path).convert_alpha(), (300, 90))
        self.r_image = pygame.transform.rotate(self.image, 90)
        
        
        self.rect = self.image.get_rect(topleft=position)

        self.rotated = False

    def rotate(self):
        pos = self.get_position()
        if self.rotated:
            self.image = self.d_image
            self.rotated = False
        else:
            self.image = self.r_image
            self.rotated = True

        self.rect = self.image.get_rect(topleft=pos )

    def get_position(self):
        return self.rect.topleft
    
    def get_surface(self):
        return self.image
    

    def draw(self, display: pygame.Surface):
        display.blit(self.image, self.rect)

class Main(PreviewMain.MainGame):
    def __init__(self) -> None:
        super().__init__()

        self.grid_size = 20

        
        self.dragging = False


        self.draw_buffer = []

        self.current_box = None
        self.current_box_position = None
        
        self.colliding_rects = []
        for i in range(3):
            item = Item(self.snap_to_grid((random.randint(0, 1200), random.randint(0, 500))))
            self.draw_buffer.append(item)
            print("Hello")
        
    def check_box(self):
        for index, r in  enumerate(self.draw_buffer):
            if r.rect.collidepoint(self.mouse_pos):
                return index
            
    def move_box(self, index):
        if index != None:
            self.draw_buffer[index].rect.move_ip(self.mouse_rel)
            print("Moving Box")
            #print(self.draw_buffer[index].get_position())         

             
    def snap_to_grid(self, pos):
        x, y = pos
        snapped_x = (x // self.grid_size) * self.grid_size
        snapped_y = (y // self.grid_size) * self.grid_size
        return (snapped_x, snapped_y)

    def draw_grid(self, display):
        width = 1280
        height = 720
        grid_color = (255, 255, 255)
        
        
        for x in range(0, width, self.grid_size):
            pygame.draw.line(display, grid_color, (x, 0), (x, height))
        for y in range(0, height, self.grid_size):
            pygame.draw.line(display, grid_color, (0, y), (width, y))
            
    def check_overlapping_bounds(self, index):
        main_box: pygame.Rect = self.draw_buffer[index].rect
        rect_buffer = [item.rect for item in self.draw_buffer if item != self.draw_buffer[index].rect]
        collision = main_box.collidelistall(rect_buffer)
        
        
        if collision != -1:
            collisions = [i for i in collision if i != index]
            if len(collisions) >= 1:
                return True
            else:
                return False
        else:
            return False
            
            

        
    def handle_events(self):
        #super().handle_events()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.current_box = self.check_box()
                if self.current_box != None:
                    self.current_box_position = self.draw_buffer[self.current_box].rect.topleft
                    self.dragging = True
                    print("grabbed " + str(self.current_box))
                    
            if event.type == pygame.MOUSEMOTION:
                if self.current_box != None:
                    self.move_box(self.current_box)     
                       
            if event.type == pygame.MOUSEBUTTONUP:
                if self.current_box != None:
                    if not self.check_overlapping_bounds(self.current_box):
                        self.draw_buffer[self.current_box].rect.topleft = self.snap_to_grid(self.draw_buffer[self.current_box].rect.topleft)
                    else:
                        self.draw_buffer[self.current_box].rect.topleft = self.snap_to_grid(self.current_box_position)
                        
                    self.current_box = None
                    self.dragging = False
                    
                    
            if event.type == pygame.KEYDOWN:
                if event.key == "r" and self.dragging:
                    print("key pressed")
                    self.draw_buffer[self.current_box].rotate()
            

    def draw(self):
        """Custom drawing logic here"""
        import math
        
        
        self.display.fill((0, 0, 0))
        self.draw_grid(self.display)
        for i in self.draw_buffer:
            i.draw(self.display)
        
        # for i in self.rect_buffer:
        #     pygame.draw.rect(self.display, (255,0,0), i)
        
        # for i in self.draw_buffer:
        #     pygame.draw.rect(self.display, (0,255,0), i.rect)
        


 
  
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
