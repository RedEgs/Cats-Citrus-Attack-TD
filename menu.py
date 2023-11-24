import pygame, sys, tween
from game import *
from main import *




class Character:
  def __init__(self, surface, x, y):
    self.sprite = surface
    self.x = x
    self.y = y

  def draw(self, surface):
    surface.blit(self.sprite, (self.x, self.y))
    
class Menu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        self.bgSprite, self.logoSprite = self.menuInit()

        self.logo = Character(self.logoSprite, 0, -1000 )
        self.time = 0.0
        self.logoTween()

    def menuInit(self):
        background = pygame.image.load("assets/main_menu/background.png").convert_alpha()
        logo = pygame.image.load("assets/main_menu/logo.png").convert_alpha()
    
        return background, logo
    
    def logoTween(self):
        self.logoAnim = tween.to(self.logo, "y", self.width//2, 3.0, "easeInOutQuad")
        print("start tween")

    
    def run(self):
        self.running = True
        while self.running:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
    def update(self):
        time = self.clock.tick(60) / 1000.0

        self.logoAnim._update(time)
        
        self.logoAnim.on_update(print("updated"))#appends a function that runs every update.


        
    def draw(self):
        self.screen.fill(0)
        self.logo.draw(self.screen)
        
        self.screen.blit(self.bgSprite, (0,0))

         

        pygame.display.flip()       




