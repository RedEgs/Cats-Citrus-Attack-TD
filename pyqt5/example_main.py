from pygame_hotreload import HotReload, set_caption     
# imports-start-hotreload
import pygame, sys, os
# imports-end-hotreload

# globals-start-hotreload
# globals-end-hotreload
class MainGame():
    # init-start-hotreload
    def __init__(self) -> None:
        print("hi")
        pygame.init()
        
        print("hi")
        self._init_display()
        print("hello")
        self.clock = pygame.Clock()
        self.run = True
        print("finito")
    # init-end-hotreload

    def _init_display(self):
        self._hwnd = None
        if len(sys.argv) > 1:
            self._hwnd = int(sys.argv[1])
            os.environ['SDL_WINDOWID'] = str(self._hwnd)
        
        self.display_width = 1280
        self.display_height = 720
        
        
        #os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (-1000, -1000)
        self.display = pygame.display.set_mode((self.display_width, self.display_height), pygame.NOFRAME)
        pygame.display.set_caption("Pygame Window")
        
    def send_event(self, type, key = None, mouse_x = None, mouse_y = None):
        if type == 1:
            event = pygame.event.Event(pygame.KEYDOWN, key=key)
            pygame.event.post(event)
        elif type == 2:
            last_pos = (mouse_x, mouse_y)
            
            
            if last_pos:
                rel_x = mouse_x - last_pos[0]
                rel_y = mouse_y - last_pos[1]
            else:
                rel_x, rel_y = 0, 0

            last_pos = (mouse_x, mouse_y)
            
            
            event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (mouse_x, mouse_y), 'rel': (rel_x, rel_y), 'buttons': pygame.mouse.get_pressed()})
            pygame.event.post(event)
            pygame.mouse.set_pos(mouse_x, mouse_y)
        
            
        
        
        
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.MOUSEMOTION: 
                self.mouse_pos = event.pos
                #print(self.mouse_pos)
                
                #pygame.draw.circle(self.display, (0, 0, 255), event.pos, 20)
            
            
    def update(self):
        # Input updating logic here
        pass
    
    def draw(self):
        # Input drawing logic here
        self.display.fill((200, 255, 0))
        
        try:
            pygame.draw.circle(self.display, (255, 0, 0), self.mouse_pos, 20)
        except: pass
        
        pygame.display.flip()
    
    # loop-start-hotreload
    def run_game(self):
        while self.run:
            self.clock.tick()
            self.handle_events()
            self.update()
            self.draw()
            
            #yield self.display

        pygame.quit()
        sys.exit()
    # loop-end-hotreload
    
        
    def close_game(self):
        self.run = False
        pygame.quit()
    

 
e = MainGame()
e.run_game()