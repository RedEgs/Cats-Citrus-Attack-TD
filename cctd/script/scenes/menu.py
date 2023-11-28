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

        self.width, self.height = self.screen.get_size()
        self.center_x = self.width // 2
        self.center_y = self.height // 2

        self.bgImage, self.logoImage, self.loadingImage = self.menuInit()

        self.bgSprite = TweenOpacity(
            0, 255, self.bgImage, 1, pytweening.easeInOutQuad)
        self.bgSprite.start()
        self.logoSprite = TweenSprite(
            start_pos=(self.width - 800, -800),
            end_pos=(0, -150),
            image=self.logoImage,
            duration=3,
            easing_function=pytweening.easeInOutCubic)
        self.loadingSprite = TweenOpacity(
            0, 255, self.loadingImage, 1, pytweening.easeInOutQuad)

        self.playButton = Button(
            self.center_x, self.center_y+500, os.path.join(resources_dir, "main_menu", "play_button_off.png"), os.path.join(resources_dir, "main_menu", "play_button_on.png"), self.playGame)
        self.playButton.tween_pos(
            (self.center_x, self.center_y), 5, 2, pytweening.easeInOutCubic)

        self.optionsButton = Button(
            self.center_x, self.center_y+500, os.path.join(resources_dir, "main_menu", "options_button_off.png"), os.path.join(resources_dir, "main_menu", "options_button_on.png"), self.callback)
        self.optionsButton.tween_pos(
            (self.center_x, self.center_y+75), 5, 2.5, pytweening.easeInOutCubic)

        self.quitButton = Button(
            self.center_x, self.center_y+500, os.path.join(resources_dir, "main_menu", "quit_button_off.png"), os.path.join(resources_dir, "main_menu", "quit_button_on.png"), quitGame)
        self.quitButton.tween_pos(
            (self.center_x, self.center_y+150), 5, 3, pytweening.easeInOutCubic)

    def callback(self):
        print("pressed")

    def playGame(self):
        self.scene_director.switch_scene("lobby_scene")

    def menuInit(self):
        background = pygame.image.load(
            os.path.join(resources_dir, "main_menu", "background.png")).convert_alpha()
        logo = pygame.image.load(os.path.join(resources_dir, "main_menu", "logo.png")).convert_alpha()
        loadingScreen = pygame.image.load(
            os.path.join(resources_dir, "loading", "loading_screen.png")).convert_alpha()

        return background, logo, loadingScreen

    def on_exit(self):
        print("Left Menu")

    def on_enter(self):
        print("Entered Menu")
   
    def run(self, event):
        self.events(event)
        self.update()
        self.draw()

    def events(self, event):
        self.playButton.handle_event(event)
        self.optionsButton.handle_event(event)
        self.quitButton.handle_event(event)

    def update(self):
        self.bgSprite.update()
        self.loadingSprite.update()
        self.logoSprite.update()

        self.playButton.update()
        self.optionsButton.update()
        self.quitButton.update()

    def draw(self):
        self.screen.fill(0)

        self.bgSprite.draw(self.screen)
        self.logoSprite.draw(self.screen)

        self.playButton.draw(self.screen)
        self.optionsButton.draw(self.screen)
        self.quitButton.draw(self.screen)

        self.loadingSprite.draw(self.screen)
