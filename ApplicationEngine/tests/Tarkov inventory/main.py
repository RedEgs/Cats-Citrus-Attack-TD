# Main project file
import pygame, sys, os, random, pathlib
from pyredengine import PreviewMain # type: ignore


class Item:
    def __init__(self, position: pygame.Vector2) -> None:
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
    def __init__(self, fullscreen = False) -> None:
        super().__init__(fullscreen)

        if self._engine_mode:
            abspath = os.path.abspath(__file__)
            dname = os.path.dirname(abspath)
            os.chdir(dname)

        self.grid_size = 10
        self.dragging = False
        
        self.draw_buffer = []
        
        # HOTSAVE
        self.draw_positions = []

        self.current_box = None
        self.mouse_pos = (0,0)
        self.test_string = "Hello World"

        self.colliding_rects = []
        for _ in range(5):
            item = Item(self.snap_to_grid((random.randint(0, 1200), random.randint(0, 500))))
            self.draw_buffer.append(item)
            self.draw_positions.append(item.rect)
        
    def check_box(self):
        for index, r in  enumerate(self.draw_buffer):
            if r.rect.collidepoint(self.mouse_pos):
                return index
            
    def move_box(self, index):
        if index != None:
            self.draw_buffer[index].rect.move_ip(self.mouse_rel)
            #print(self.draw_buffer[index].get_position())         

             
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
            
    def check_overlapping_bounds(self, index):
        main_box: pygame.Rect = self.draw_buffer[index].rect
        rect_buffer = [item.rect for item in self.draw_buffer if item != self.draw_buffer[index].rect]
        collision = main_box.collidelistall(rect_buffer)


        if collision != -1:
            collisions = [i for i in collision if i != index]
            return len(collisions) >= 1
        else:
            return False
            
            

        
    def handle_events(self):  # sourcery skip: swap-nested-ifs
        #super().handle_events()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = event.pos

                self.current_box = self.check_box()
                if self.current_box != None:
                    self.current_box_position = self.draw_buffer[self.current_box].rect.topleft
                    self.dragging = True
                    print(f"grabbed {str(self.current_box)}")

            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                self.mouse_rel = event.rel

                if self.current_box != None:
                    self.move_box(self.current_box)     

            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pos = event.pos
                if self.current_box != None:
                    if not self.check_overlapping_bounds(self.current_box):
                        self.draw_buffer[self.current_box].rect.topleft = self.snap_to_grid(self.draw_buffer[self.current_box].rect.topleft)
                    else:
                        self.draw_buffer[self.current_box].rect.topleft = self.snap_to_grid(self.current_box_position)

                    self.current_box = None
                    self.dragging = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.dragging:
                    print("key pressed")
                    self.draw_buffer[self.current_box].rotate()
                

    def draw(self):
        """Custom drawing logic here"""
        import math
        
        if self._engine_mode:
            self.display.fill((20, 100, 180))
        else:
            self.display.fill((180, 100, 20))
        self.draw_grid(self.display)
        
        for index, i in enumerate(self.draw_buffer):
            self.display.blit(i.image, self.draw_positions[index])
        # self.display.fblits([(i.image, i.rect) for i in self.draw_buffer])

        font = pygame.font.Font(pygame.font.get_default_font(), 36)

        # now print the text
        text_surface = font.render(self.test_string, antialias=True, color=(0, 0, 0))
        self.display.blit(text_surface, dest=(0,0))
            
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