# Main project file
import pygame, sys, os, random
from pyredengine import PreviewMain

class Main(PreviewMain.MainGame):
    def __init__(self) -> None:
        super().__init__()


    
          
    def handle_events(self):
        #super().handle_events()
        for event in pygame.event.get():
           pass
        
    def update(self):
        pass

    def draw(self):
        """Custom drawing logic here"""
        import math
        
        
        self.display.fill((20, 100, 180))

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