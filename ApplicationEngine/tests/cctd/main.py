 # Main project file
import pygame, os, ast, math, time # type: ignore
from pyredengine import PreviewMain # type: ignore
from pyredengine import SceneService # type: ignore
from libs.cctd import * # type: ignore
from libs.gui import * # type: ignore

"""
All code given is the bare minimum to safely run code within the engine.
Removing any code that already exists in not recommended and you WILL run into issues.
When compiled, parts of code are removed to optimise and simplify the file.
"""



class MainMenu(Scene):
    def __init__(self, display: pygame.Surface):
        super().__init__(self)
        self.display = display

        centerx = self.display.get_size()[0]//2
        centery = self.display.get_size()[1]//2

        self.PlayButton = Button((centerx, centery), (300, 100))

    def on_enter(self):
        print("entered")

    def handle_events(self, event: pygame.event.Event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.PlayButton.is_clicked(mouse_pos):
                pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1, {"Scene": "Game"}))

    def update(self):
        pass

    def draw(self):
        self.PlayButton.draw(self.display)

class Game(Scene):
    def __init__(self, display: pygame.Surface):
        super().__init__(self)

        self.display =  display

        self.LivesCount = 100
        self.Cash = 100
        self.MaxTowers = 5
        self.Round = 1

        self.enemy_list = []
        self.gui_list = []

        self.damage_text_list = []
        self.tower_panel_list = []

        self.GameMap = GameMap("map1")
        self.RoundManager = RoundManager(self.Round, self.Cash, self.GameMap, self.enemy_list)

        self.LivesText = Text(f"Lives: {self.LivesCount}", 24, (10, 10))
        self.MoneyText = Text(f"Cash: ${self.Cash}", 24, (230, 10))
        self.RoundText = Text(f"Round: {self.Round}/100", 24, (10, 45))
        self.TowerPanel = None

        self.tower_list = []
        self.debug_mode = False

        self.gui_list.append(self.LivesText)
        self.gui_list.append(self.MoneyText)
        self.gui_list.append(self.RoundText)

    def on_enter(self):
        pass

    def handle_events(self, event: pygame.event.Event, mouse_pos):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if self.Cash - 20 < 0: return

                tower = Tower(mouse_pos, self.tower_list)
                tower.button = Button(tower.pos, tower.rect.size)
                self.tower_list.append(tower)
                if tower.check_overlap(self.GameMap.get_mask(), (0,0)) or len(self.tower_list) > 5:
                    self.tower_list.remove(tower)
                    return

                self.RoundManager.spend_money(20, self.MoneyText)


            if event.key == pygame.K_SPACE:
                self.RoundManager.start_round()
                # Spawning Logic

        if event.type == pygame.MOUSEBUTTONDOWN:
            for tower in self.tower_list:
                btn = tower.button
                if btn.is_clicked(mouse_pos) and self.TowerPanel == None:


                    TowerPanel = Panel(
                        (self.display.get_size()[0]-200,  (self.display.get_size()[1])//2),
                        (350, self.display.get_size()[1]-50),
                    )

                    tl = TowerPanel.rect.topleft
                    tr = TowerPanel.rect.topright
                    tm = ((tl[0] + tr[0]) / 2, (tl[1] + tr[1]) / 2)

                    TowerText = Text(tower.tower_name, 26, (0,0))
                    TowerText.rect.center = (tm[0], tm[1]+100)

                    self.gui_list.append(TowerPanel)
                    self.gui_list.append(TowerText)
                    self.tower_panel_list.append(TowerPanel)
                    self.tower_panel_list.append(TowerText)






                elif btn.is_clicked(mouse_pos) and self.TowerPanel != None:
                    self.gui_list.remove(self.TowerPanel)
                    self.TowerPanel = None

        if event.type == pygame.MOUSEBUTTONUP:
            print("heello")

        for gui in self.gui_list:
            gui.handle_events(event, mouse_pos)


    def on_tower_damage(self, target = None, damage = None):
        if target == None: return


        text = Text(f"-{damage}", 14, target.rect.center)
        self.gui_list.append(text)
        self.damage_text_list.append(text)

    def update(self):
        self.current_time = pygame.time.get_ticks()
        for enemy in self.enemy_list:
            if enemy.update() == True:
                self.LivesCount -= 1
                self.LivesText.update_text(f"Lives: {self.LivesCount}")

                if self.LivesCount <= 1:
                    self.run = False

        self.RoundManager.update(self.current_time, self.RoundText, self.MoneyText)

        # Check if it's time to spawn an enemy
        for tower in self.tower_list:
            tower.update(self.enemy_list, self)

        self.Round = self.RoundManager.RoundCount
        self.Cash = self.RoundManager.MoneyCount

    def draw(self):
        self.display.blit(self.GameMap.get_surface())

        if self.debug_mode:
            # if self.draw_mask:
            #     self.display.blit(self.GameMap.mask_texture)

            for i, obj in enumerate(self.GameMap.waypoints):
                if i == 0:
                    pygame.draw.circle(self.display, (0, 0, 255),  obj, 10)
                elif i == len(self.GameMap.waypoints)-1:
                    pygame.draw.circle(self.display, (0, 255, 255), obj, 10)
                else:
                    pygame.draw.circle(self.display, (255, 255, 0), obj, 10)

            self.GameMap.draw_points(self.display)

        for enemy in self.enemy_list:
            enemy.draw(self.display)

        for tower in self.tower_list:
            tower.draw(self.display)

        for gui in self.gui_list:
            if isinstance(gui, Text) and gui in self.damage_text_list:
                gui.pos = (gui.pos[0], gui.pos[1]-0.5)
                gui.rect.center = gui.pos

                if self.current_time - gui.created_time >= 500:
                    self.damage_text_list.remove(gui)
                    self.gui_list.remove(gui)

            gui.draw(self.display)




class Main(PreviewMain.MainGame):
    def __init__(self, fullscreen = False) -> None:
        super().__init__(fullscreen)
        """
        Make sure not to remove the super() method above, as it will break the whole script.
        """

        self.display = pygame.display.get_surface()
        if self._engine_mode:
            abspath = os.path.abspath(__file__)
            dname = os.path.dirname(abspath)
            os.chdir(dname)

        # --------------------------
        self.MainMenu = MainMenu(self.display)
        self.Game = Game(self.display)

        self.Scenes = {
            "Game": self.Game,
            "MainMenu": self.MainMenu
        } #[PUBLIC]

        self.CurrentScene: Scene = self.MainMenu #[PUBLIC]
        #--------------------------



        # -------------





    def handle_events(self):
        """
        All your logic for handling events should go here.
        Its recommended you write code to do with event handling here.
        Make sure that you don't remove the `pygame.QUIT` event as the game won't be able to be shutdown.
        See pygame docs for more info: https://www.pygame.org/docs/ref/event.html.
        """
        scene_switch_event = pygame.USEREVENT + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == scene_switch_event:
                self.CurrentScene = self.Scenes[event.Scene]
                self.CurrentScene.on_enter()

            self.CurrentScene.handle_events(event, self.mouse_pos)


    def update(self):
        """
        This is where you independant code goes.
        This is purely a conceptual seperator from the rest of the game code.
        Think of this as the "body" of your program.
        """
        self.CurrentScene.update()


    def draw(self):
        """
        This is where your drawing code should do.
        Make sure that `pygame.display.flip()` is the last line.
        Make sure that `self.display.fill()` is at the start too.

        """



        self.display.fill((180, 100, 20))

        self.CurrentScene.draw()


        pygame.display.flip()
