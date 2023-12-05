import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.gui import *
from ..libs.utils import *
from ..libs.scenes import *



class Menu(Scene):
    def __init__(self, screen, scene_director, scene_name):
        super().__init__(screen, scene_director, scene_name)

        self.screen = screen
        self.scene_director = scene_director
        self.scene_name = scene_name

        self.tween_director = TweenDirector()

        self.width, self.height = self.screen.get_size()
        self.center_pos = (self.width //2, self.height // 2)        

        self.background_image = load_image(os.path.join(current_dir, '..', '..', 'resources', 'main_menu', 'background.png'))
        self.background_image.set_alpha(0)
        
        
        self.background_image_tween = Tween(opacity_fade_in_data, self.tween_director)
        self.background_image_tween.start()

        self.logo_image = load_image(os.path.join(current_dir, '..', '..', 'resources', 'main_menu', 'logo.png'))
        






        # background positions : (0,0) | background alpha: 0, 255
        # logo positions : (self.width - 800, -800), (0, -150)
        
        # play button: (self.center_x, self.center_y+500), (self.center_x, self.center_y)
        # options button: (self.center_x, self.center_y+500), (self.ceqnter_x, self.center_y+75)
        # quit buttons: (self.center_x, self.center_y+500), (self.center_x, self.center_y+150)

    def playGame(self):
        self.scene_director.switch_scene("lobby_scene")


    def on_exit(self):
        pass

    def on_enter(self):
        pass
        
   
    def run(self, event):
        self.events(event)
        self.update()
        self.draw()

    def events(self, event):
        pass

    def update(self):   
        pass    
    
    def draw(self):
        self.screen.fill(0)

        self.screen.blit(self.background_image, (0,0))
        self.tween_director.update(self.background_image.set_alpha(self.background_image_tween.get_output()))


