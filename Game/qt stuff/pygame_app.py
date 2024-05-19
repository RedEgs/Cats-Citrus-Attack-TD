import pygame
import sys
import os


class PygameWindow:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.x = 50
        self.y = 50
        self.rect_width = 40
        self.rect_height = 60
        self.vel = 5
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.color_index = 0
        self.keys_pressed = set()
        self.screen = None
        self.clock = pygame.time.Clock()
        self.run = True

        pygame.init()

        hwnd = None
        if len(sys.argv) > 1:
            hwnd = int(sys.argv[1])
            os.environ['SDL_WINDOWID'] = str(hwnd)
        
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (-1000, -1000)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
        pygame.display.set_caption("Pygame Window")

    def send_key(self, key):
        event = pygame.event.Event(pygame.KEYDOWN, key=key)
        pygame.event.post(event)
        print("sent event:" + str(event))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                print(event.key)
                #self.keys_pressed.add(event.key)
                if event.key == "a":
                    
                    self.x -= self.vel
                elif event.key == "d":
                    self.x += self.vel
                elif event.key == "w":
                    self.y -= self.vel
                elif event.key == "s":
                    self.y += self.vel
                
                
                
                
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x -= self.vel

        if keys[pygame.K_d]:
            self.x += self.vel

        if keys[pygame.K_w]:
            self.y -= self.vel

        if keys[pygame.K_s]:
            self.y += self.vel

        self.color_index = (self.color_index + 1) % len(self.colors)

    def draw(self):
        self.screen.fill(self.colors[self.color_index])
        pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.rect_width, self.rect_height))
        pygame.display.flip()

    def close_game(self):
        self.run = False
        pygame.quit()


    def run_game(self):
        while self.run:
            self.clock.tick()
            self.handle_events()
            self.update()
            self.draw()
            
            print(self.clock.get_fps())
            yield self.screen

        pygame.quit()
        sys.exit()
        
    def get_screen(self):
        return self.screen


# if __name__ == "__main__":
#     game = PygameWindow()
#     game.run_game()
