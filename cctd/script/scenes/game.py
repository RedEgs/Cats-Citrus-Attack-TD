import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.scenes import *
from ..libs.map import *
from ..libs.gui import *
from ..libs.towers import *
from ..libs.shop import *
class EndlessGameScene(Scene):
    def __init__(self, screen, scene_director, scene_name):
        super().__init__(screen, scene_director, scene_name)

        self.screen = screen
        self.scene_director = scene_director
        self.scene_name = scene_name
        
        self.game = Game()
        
        # Load the map
        self.map_director = MapDirector(screen)
        self.map = self.map_director.load_map(self.map_director.all_maps[0])
        
        self.shop = Shop()
    
    
    
        #self.tower_director = TowerDirector(self.map)
        
        # Load the GUI Overlay
        overlay_image = os.path.join(os.path.join(current_dir, '..', '..', 'resources', "game_overlay", 'game_menu.png'))
        self.game_overlay = GameOverlay(0, 0, overlay_image)
        
        # Load start button
        self.round_button = Button(
            300, 516+500, os.path.join(resources_dir, "game_overlay", "round_button_off.png"), os.path.join(resources_dir, "game_overlay", "round_button_on.png"), self.callback)
        self.round_button.tween_pos(
            (300, 516), 2, 0, pytweening.easeInOutCubic)  
        
        self.purchase_button = Button(
            700, 310+500, os.path.join(resources_dir, "game_overlay", "purchase_button_off.png"), os.path.join(resources_dir, "game_overlay", "purchase_button_on.png"), self.callback)
        self.purchase_button.tween_pos(
            (700, 310), 2, 0, pytweening.easeInOutCubic)  
        
        
         
        # Cash Text
        self.money_text = GUIText(20, (255,255,255), (15 ,10))
        self.money_text.outline_text("$:", "black")
        
    def callback(self):
        print("Pressed")
        
    def on_exit(self):
        return super().on_exit()

    def on_enter(self):
        return super().on_enter()
    
    def events(self, event):
        self.round_button.handle_event(event)
        self.purchase_button.handle_event(event)
        self.shop.handle_event(event)
        #self.tower_director.handle_event(event)

    def update(self):
        self.game.update()
        #self.tower_director.update()
        self.shop.update()
        
        self.purchase_button.update()
        self.round_button.update()

    def draw(self):
        self.map.draw(self.screen)
        self.game_overlay.draw(self.screen)
        #self.tower_director.draw(self.screen)
        self.shop.draw(self.screen)
        
        
        self.round_button.draw(self.screen)
        self.purchase_button.draw(self.screen)

        self.money_text.draw(self.screen)


    def run(self, event):
        self.events(event)
        self.update()
        self.draw()

    def get_scene_info(self):
        return self.scene_name

class Game:
    def __init__(self):

        # Player Variables
        self.health = 100.0
        self.current_round = 0
        
        self.first_round = True

    def on_end_round(self):
        pass
    
    def on_start_round(self):
        pass

    def update(self):
        pass
    


























"""
class Game(Scene):
    def __init__(self, screen, scene_director):
        super().__init__(screen, scene_director)


        # Load the map from a file (adjust the filename, width, and height accordingly)
        self.map = Map(
            'map1.png', self.render_width, self.render_height)
        self.map_mask = self.map.map_mask
        self.map.load_waypoints("waypoints.txt")

        # Create a grid with a specified render size (adjust as needed)
        self.grid = Grid(cellSize, self.render_width, self.render_height)
        # Pass the grid instance to GridOverlay
        self.grid_overlay = GridOverlay(self.grid)
        self.path_overlay = PathOverlay(self.map.waypoints)
        self.mousePreview = MousePreviewOverlay(
            (48, 48), "tower.png", 200)

        self.show_debugs = True
        self.grid_enabled = True
        self.editorMode = True

        self.load()
        self.gui()

    def load(self):
        self.enemy_group = pygame.sprite.Group()

        self.enemy = Enemy(self.map.waypoints)
        self.enemy_group.add(self.enemy)

        self.tower_group = pygame.sprite.Group()

    def gui(self):
        self.manager = pygui.UIManager(
            (self.width, self.height), "themes.json")

        side_panel = pygui.elements.UIPanel(
            relative_rect=pygame.Rect(599, 0, 201, self.height),
            starting_height=0,
            manager=self.manager)

        self.fpsCounter = FPSCounter(self.manager, self.clock)
        self.editorOverlay = EditorModeOverlay(self.manager, self.editorMode)
        self.gridResOverlay = GridResOverlay(
            self.manager, self.grid.get_grid_res())
        self.enemyOverlay = EnemyOverlay(self.manager, len(self.enemy_group))
        self.preview_tower = self.mousePreview

    def run(self, event):
        time_delta = self.clock.tick(FPS) / 1000.0
        self.events(event)
        self.update(time_delta)
        self.draw()
        self.gameplay()

    def events(self, event):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouseX, mouseY = pygame.mouse.get_pos()
                    gridX, gridY = positionOnGrid(mouseX, mouseY, cellSize)

                    # Query the cell when clicked
                    clicked_cell = self.grid.get_hovered_cell(mouseX, mouseY)

                    new_tower = placeTower(
                        self.tower_group, self.preview_tower, self.map_mask)
                    if new_tower:
                        print(
                            f"Tower placed at ({new_tower.rect.x}, {new_tower.rect.y})")

                    # if clicked_cell:

                if event.button == 3:
                    if self.editorMode:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            mouseX, mouseY = pygame.mouse.get_pos()
                            rounded_coordinates = self.map.get_rounded_coordinates(
                                mouseX, mouseY)
                            if rounded_coordinates in self.map.waypoints:
                                self.map.waypoints.remove(rounded_coordinates)
                        else:
                            mouseX, mouseY = pygame.mouse.get_pos()
                            rounded_coordinates = self.map.get_rounded_coordinates(
                                mouseX, mouseY)
                            print(
                                f"Rounded Coordinates on Right-Click: {rounded_coordinates}")
                            self.map.add_waypoint(rounded_coordinates)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.grid_enabled = not self.grid_enabled
                if event.key == pygame.K_F7:
                    self.editorMode = not self.editorMode
                    self.editorOverlay.update(self.editorMode)

                if event.key == pygame.K_F3:
                    self.show_debugs = not self.show_debugs

                    if self.show_debugs:
                        self.fpsCounter.show()
                        self.editorOverlay.show()
                        self.enemyOverlay.show()
                        self.gridResOverlay.show()
                    else:
                        self.fpsCounter.hide()
                        self.editorOverlay.hide()
                        self.enemyOverlay.hide()
                        self.gridResOverlay.hide()

                if self.editorMode:
                    if event.key == pygame.K_F5:
                        self.map.save_map("waypoints.txt")
                        print("Saved Map")

            elif event.type == pygame.MOUSEMOTION:
                self.mousePreview.update_position()

            self.manager.process_events(event)

    def gameplay(self):
        self.enemy_group.update()

    def update(self, time_delta):
        # Update hover state
        mouseX, mouseY = pygame.mouse.get_pos()
        self.grid.update_hover(mouseX, mouseY)

        self.manager.update(time_delta)

        self.fpsCounter.update()
        self.gridResOverlay.update()
        self.enemyOverlay.update(len(self.enemy_group))
        self.preview_tower.update_position()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.map.draw(self.screen)

        # Draw the Grid from the loaded map
        self.grid.draw_within_map_bounds(
            self.screen, self.render_width, self.render_height, self.show_debugs)
        self.map.draw(self.screen)

        if self.show_debugs:
            self.map_mask_surface = self.map_mask.to_surface()
            self.screen.blit(self.map_mask_surface, (0, 0))
            self.path_overlay.draw(self.screen)

        if self.grid_enabled:
            self.grid_overlay.draw(self.screen)

        self.enemy_group.draw(self.screen)
        self.tower_group.draw(self.screen)

        self.manager.draw_ui(self.screen)
        self.mousePreview.draw(self.screen, self.tower_group, self.map_mask)

        # Update The Display
        pygame.display.update()
"""