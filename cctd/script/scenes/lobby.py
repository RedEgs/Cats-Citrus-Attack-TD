import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.gui import *
from ..libs.utils import *
from ..libs.scenes import *
from ..libs.map import *


class LobbyScene(Scene):
    def __init__(self, screen, scene_director, scene_name):
        super().__init__(screen, scene_director, scene_name)

        self.screen = screen
        self.scene_director = scene_director
        self.scene_name = scene_name
        
        self.map_director = MapDirector(screen)

        self.width, self.height = self.screen.get_size()
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        
        
        self.playButton = Button(
            self.center_x, self.center_y+200, os.path.join(resources_dir, "lobby", "endless_button_off.png"), os.path.join(resources_dir, "lobby", "endless_button_on.png"), self.playGame)
        self.background = pygame.image.load(
            os.path.join(resources_dir, "main_menu", "background.png")).convert_alpha()

    def playGame(self):
        print("Clicked")
        self.scene_director.switch_scene("game_scene")


    def on_exit(self):
        return super().on_exit()

    def on_enter(self):
        return super().on_enter()
    
    def events(self, event):
        self.playButton.handle_event(event)

    def update(self):
        self.playButton.update()

    def draw(self):
        self.screen.fill(0)
        
        self.screen.blit(self.background, (0,0))
        self.playButton.draw(self.screen)

    def run(self, event):
        self.events(event)
        self.update()
        self.draw()

    def get_scene_info(self):
        return self.scene_name