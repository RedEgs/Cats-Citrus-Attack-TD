import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.gui import *
from ..libs.utils import *
from ..libs.scenes import *

class Menu(Scene):
    def __init__(self, screen, scene_director, scene_name):
        super().__init__(screen, scene_director, scene_name)
        self.gui_director = GUIDirector()

        self.screen = screen
        self.scene_director = scene_director
        self.scene_name = scene_name

        self.tween_director = TweenDirector()

        self.width, self.height = self.screen.get_size()
        self.center_pos = (self.width //2, self.height // 2)        

        #SECTION - Images and tweening
        
        # Background Image Tweening
        self.background_image = load_image(os.path.join(current_dir, '..', '..', 'resources', 'main_menu', 'background.png'))
        self.background_image.set_alpha(0)
        self.background_image_tween = Tween(opacity_fade_data, self.tween_director)
        self.background_image_tween.start()
        
        # Logo Image Tweening
        self.logo_image = load_image(os.path.join(current_dir, '..', '..', 'resources', 'main_menu', 'logo.png'))
        self.logo_image_tween = TweenVector2(TweenData((self.width - 800, -800), (0, 0), 2, 0, pytweening.easeInOutCubic), self.tween_director)
        self.logo_image_tween.start()
        
        #!SECTION
        
        #SECTION - Buttons
        self.play_button = Button(self.gui_director, (self.center_pos[0], self.center_pos[1]+500), os.path.join(current_dir, '..', '..', 'resources', 'main_menu', 'play_button_off.png'),  lambda: self.scene_director.switch_scene("lobby_scene"), lambda: None)
        
        self.play_button_tween = TweenVector2(TweenData((self.center_pos[0], self.center_pos[1]+500), (self.center_pos[0], 330), 2, .5, pytweening.easeInOutCubic), self.tween_director)
        self.play_button_tween.start()
        
        
        self.options_button = Button(self.gui_director, (self.center_pos[0], self.center_pos[1]+500), os.path.join(current_dir, '..', '..', 'resources', 'main_menu', 'options_button_off.png'), lambda: print("Left Clicked"), lambda: None)
        self.options_button_tween = TweenVector2(TweenData((self.center_pos[0], self.center_pos[1]+500), (self.center_pos[0], 400), 2, .75, pytweening.easeInOutCubic), self.tween_director)
        self.options_button_tween.start()
        
        self.quit_button = Button(self.gui_director, (self.center_pos[0], self.center_pos[1]+500), os.path.join(current_dir, '..', '..', 'resources', 'main_menu', 'quit_button_off.png'), quitGame, lambda: None)
        self.quit_button_tween = TweenVector2(TweenData((self.center_pos[0], self.center_pos[1]+500), (self.center_pos[0],  472), 2, 1, pytweening.easeInOutCubic), self.tween_director)
        self.quit_button_tween.start()
        
        #!SECTION
        
        # background positions : (0,0) | background alpha: 0, 255 - 
        # logo positions : (self.width - 800, -800), (0, -150)
        
        # play button: (self.center_x, self.center_y+500), (self.center_x, self.center_y)
        # options button: (self.center_x, self.center_y+500), (self.ceqnter_x, self.center_y+75)
        # quit buttons: (self.center_x, self.center_y+500), (self.center_x, self.center_y+150)        

    def on_exit(self):
        pass

    def on_enter(self):
        pass
        
   
    def run(self, event):
        self.events(event)
        self.update()
        self.draw()

    def events(self, event):
        self.play_button.handle_event(event)
        self.options_button.handle_event(event)
        #self.quit_button.handle_event(event)
        
        pass

    def update(self):   
        pass    
    
    def draw(self):
        self.screen.fill(0)

        self.screen.blit(self.background_image, (0,0))


