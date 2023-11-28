import pytweening, pygame, sys, os

#cur_dir = os.path.dirname(os.path.realpath(__file__))
#libs_dir = os.path.join(cur_dir, 'subdirectory')
#sys.path.append(libs_dir)


from ..libs.utils import *
from ..libs.scenes import *



class Menu(Scene):
    def __init__(self, screen, event, scene_director, scene_name):
        super().__init__(screen, event, scene_director, scene_name)

        self.screen = screen
        self.event = event
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
            self.center_x, self.center_y+500, "assets/main_menu/play_button_off.png", "assets/main_menu/play_button_on.png", self.playGame)
        self.playButton.tween_pos(
            (self.center_x, self.center_y), 5, 2, pytweening.easeInOutCubic)

        self.optionsButton = Button(
            self.center_x, self.center_y+500, "assets/main_menu/options_button_off.png", "assets/main_menu/options_button_on.png", self.callback)
        self.optionsButton.tween_pos(
            (self.center_x, self.center_y+75), 5, 2.5, pytweening.easeInOutCubic)

        self.quitButton = Button(
            self.center_x, self.center_y+500, "assets/main_menu/quit_button_off.png", "assets/main_menu/quit_button_on.png", self.quitGame)
        self.quitButton.tween_pos(
            (self.center_x, self.center_y+150), 5, 3, pytweening.easeInOutCubic)

    def callback(self):
        print("pressed")

    def playGame(self):
        self.loadingSprite.start()
        # self.scene_director.switch_scene("debug_scene")

    def quitGame(self):
        pygame.quit()
        sys.exit()

    def menuInit(self):
        background = pygame.image.load(
            "assets/main_menu/background.png").convert_alpha()
        logo = pygame.image.load("assets/main_menu/logo.png").convert_alpha()
        loadingScreen = pygame.image.load(
            "assets/loading/loading_screen.png").convert_alpha()

        return background, logo, loadingScreen

    def run(self, event):
        super().__init__()
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
