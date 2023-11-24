# game.py
import pygame
import sys
from map import Map
from debugs import *
from grid import positionOnGrid, Grid, GridCell
from enemy import Enemy
from towers import Tower, placeTower
import pygame_gui as pygui

FPS = 60
cellSize = 20


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        self.render_size = 30
        self.render_width = self.render_size
        self.render_height = self.render_size

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

    def run(self):
        self.playing = True
        while self.playing:
            time_delta = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update(time_delta)
            self.draw()
            self.gameplay()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
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
