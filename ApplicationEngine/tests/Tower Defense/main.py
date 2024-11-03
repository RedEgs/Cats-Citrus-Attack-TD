# Main project file
import pygame, os
from pyredengine import PreviewMain # type: ignore

class Player:
    def create_player_tex(self):
        surf = pygame.Surface((50, 50))
        surf.fill(pygame.Color(255, 255, 255))
        
        return surf
    
    def __init__(self):
        self.pos = [0, 0]
        self.sprite = self.create_player_tex()
        
        self.player_speed = 1
        
        
        
        self.moving_up = self.moving_down = self.moving_left = self.moving_right = False

        
    
    def player_inputs(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.moving_up = True
            elif event.key == pygame.K_s:
                self.moving_down = True
            elif event.key == pygame.K_a:
                self.moving_left = True
            elif event.key == pygame.K_d:
                self.moving_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.moving_up = False
            elif event.key == pygame.K_s:
                self.moving_down = False
            elif event.key == pygame.K_a:
                self.moving_left = False
            elif event.key == pygame.K_d:
                self.moving_right = False
    
    def update_movement(self):
        if self.moving_up:
            self.pos[1] -= self.player_speed
        if self.moving_down:
            self.pos[1] += self.player_speed
        if self.moving_left:
            self.pos[0] -= self.player_speed
        if self.moving_right:
            self.pos[0] += self.player_speed
    
    def draw_player(self, display: pygame.Surface):
        display.blit(self.sprite, self.pos)





class Main(PreviewMain.MainGame):
    def __init__(self, fullscreen = False) -> None:
        super().__init__(fullscreen)

        self.display = pygame.display.get_surface()
        
        if self._engine_mode:
            abspath = os.path.abspath(__file__)
            dname = os.path.dirname(abspath)
            os.chdir(dname)
            
        self.player = Player()
        self.player_pos = self.player.pos #[PUBLIC]
            
        
            
            
            
            
            
            
            
        
    def handle_events(self): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            self.player.player_inputs(event)
               
    def update(self):
        pass

    def draw(self):
        self.display.fill((18,18,18))

        self.player.update_movement()
        self.player.draw_player(self.display)
        
        
        
        pygame.display.flip()
    
    