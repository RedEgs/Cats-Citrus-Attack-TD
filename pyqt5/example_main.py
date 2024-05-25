import pygame, sys, os

class MainGame():
    def __init__(self) -> None:
        pygame.init()
        
        self._init_display()
        self.clock = pygame.Clock()
        self.run = True

    def _init_display(self):
        self._hwnd = None
        if len(sys.argv) > 1:
            self._hwnd = int(sys.argv[1])
            os.environ['SDL_WINDOWID'] = str(self._hwnd)
        
        self.display_width = 1280
        self.display_height = 720
        
        
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (-1000, -1000)
        self.display = pygame.display.set_mode((self.display_width, self.display_height), pygame.NOFRAME)
        pygame.display.set_caption("Pygame Window")
        
    def send_key(self, key):
        event = pygame.event.Event(pygame.KEYDOWN, key=key)
        pygame.event.post(event)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def update(self):
        # Input updating logic here
        pass
    
    def draw(self):
        # Input drawing logic here
        pygame.display.flip()
    
    def run_game(self):
        while self.run:
            self.clock.tick()
            self.handle_events()
            self.update()
            self.draw()
            
            yield self.display

        pygame.quit()
        sys.exit()
        
    def close_game(self):
        self.run = False
        pygame.quit()

