import pytweening, pygame, sys, os

import engine.libs.Maths as Maths
import engine.libs.Utils as utils
import engine.libs.EntityService as EntityService 
import engine.libs.SceneService as SceneService 
import engine.libs.GuiService as GuiService 
import engine.libs.TweenService as TweenService

from engine.libs import CameraModule, GridModule, ParticleModule, SpecialEffectsModule
from engine.libs import GuiLiteModule as glm

from cctd.scripts import map_loader
from cctd.scripts import tower_handler as th



class Workshop(SceneService.Scene):
    def __init__(self, scene_name, app):
        super().__init__(scene_name, app)
        self.app = app
        self.camera = CameraModule.CameraComponent(app, pygame.Rect(0, 0, 1280, 720))
    
        self.tower_selection_panel_tween = TweenService.Tween(pygame.Vector2(950, 30), pygame.Vector2(1500, 30), 1, pytweening.easeInOutCubic)
        self.tower_selection_panel = GuiService.PanelElement(GuiService.GuiSpaces.SCREEN,
                                                             self.camera,
                                                             (self.tower_selection_panel_tween.get_output()), 
                                                             (300, 660),
                                                             (161, 150, 133),
                                                             drop_shadow=False,
                                                             shadow_size=5,
                                                             rounded=True,
                                                             outline=True,
                                                             outline_color=(0,0,0),
                                                             outline_thickness=4)

        self.enemy_selection_panel_tween = TweenService.Tween(pygame.Vector2(30, 500), pygame.Vector2(30, 900), 1, pytweening.easeInOutCubic)
        self.enemy_selection_panel = GuiService.PanelElement(GuiService.GuiSpaces.SCREEN,
                                                             self.camera,
                                                             (self.enemy_selection_panel_tween.get_output()), 
                                                             (900, 190),
                                                             (161, 150, 133),
                                                             drop_shadow=False,
                                                             shadow_size=5,
                                                             rounded=True,
                                                             outline=True,
                                                             outline_color=(0,0,0),
                                                             outline_thickness=4)

        self.tower_manager = th.TowerManager()

        self.load_towers_from_directory()
        self.load_towers_on_panel()
        
        self.game_map = self.load_map()


    def events(self, event):
        key = pygame.key.get_pressed()
        # if event.type == pygame.MOUSEBUTTONDOWN:
        if key[pygame.K_w]:
            self.camera.move_up(1)
            
        elif key[pygame.K_s]:
            self.camera.move_down(1)
            
        if key[pygame.K_a]:
            self.camera.move_left(1)
         
        elif key[pygame.K_d]:
            self.camera.move_right(1)
            
        if key[pygame.K_F1]:
            if pygame.time.get_ticks() >= self.f1_pressed + 1050:
                print("pressed")
                self.f1_pressed = pygame.time.get_ticks()
                self.tower_selection_panel_tween.reverse()
        
        if key[pygame.K_F2]:
            if pygame.time.get_ticks() >= self.f2_pressed + 1050:
                print("pressed")
                self.f2_pressed = pygame.time.get_ticks()
                self.enemy_selection_panel_tween.reverse()
                
        if key[pygame.K_F3]:
            if pygame.time.get_ticks() >= self.f3_pressed + 400:
                print("pressed")
                self.f3_pressed = pygame.time.get_ticks()
                
                print(self.toggle_draw_points)
                if self.toggle_draw_points:
                    self.toggle_draw_points = False
                else:
                    self.toggle_draw_points = True
                
                

             
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.time.get_ticks() >= self.tower_button_pressed + 50:
                for btn in self.tower_buttons_group:
                    if btn.is_clicked(pygame.mouse.get_pos() - self.tower_selection_panel_tween.get_output()) and not self.selected_tower_button == btn:# 
                        self.selected_tower_button = btn
                        self.tower_button_pressed = pygame.time.get_ticks()
                        self.select_tower_from_button(btn)
                    
                    elif btn.is_clicked(pygame.mouse.get_pos() - self.tower_selection_panel_tween.get_output()) and self.selected_tower_button == btn:
                        self.tower_selected = not self.tower_selected
           
            if pygame.time.get_ticks() >= self.tower_placement_pressed + 500:
                
                
                self.tower_placement_pressed = pygame.time.get_ticks()
                
                if self.tower_manager.selected_tower and not self.tower_manager.selected_tower.preview_rect.colliderect(self.tower_selection_panel.get_rect()):
                    self.tower_manager.place_tower(self.map_image, self.map_mask, self.tower_selection_panel.get_rect())
                
            if pygame.time.get_ticks() >= self.tower_context_pressed + 500 and not self.tower_context_open:
                for tower in th.TowerManager.placed_tower_group:
                    if tower.is_over():
                        self.tower_context_pressed = pygame.time.get_ticks()
                        self.tower_context_open = True
                        
                        tower.open_tower_context()
                
            
              
    
    def on_enter(self):
        super().on_enter()
        self.f1_pressed = pygame.time.get_ticks()
        self.f2_pressed = pygame.time.get_ticks()
        self.f3_pressed = pygame.time.get_ticks()
        
        self.tower_context_open = False
        self.tower_context_pressed = pygame.time.get_ticks()
        
        self.tower_selected = False
        self.can_draw_preview = False
        
        
        self.toggle_draw_points = False
        
        self.tower_button_pressed = pygame.time.get_ticks()
        self.selected_tower_button = self.tower_buttons_group[0]
        
        self.tower_placement_pressed = pygame.time.get_ticks()
             
    def update(self):
        self.tower_selection_panel.set_screen_position(self.tower_selection_panel_tween.get_output())
        self.enemy_selection_panel.set_screen_position(self.enemy_selection_panel_tween.get_output())
        
        
        
    def draw(self, surface: pygame.Surface):
        surface.fill((2, 127, 252))
        

        surface.blit(self.map_image, (0,0))
        
        
        if self.toggle_draw_points:
            self.map_image.blit(self.map_mask.to_surface(), (0,0))  
            
            for i in self.map_waypoints:
                pygame.draw.circle(self.map_image, (255,0,0), i, 2)  
    

        self.tower_manager.draw(surface, self.map_image, self.map_mask, self.tower_selection_panel.get_rect())
        self.tower_selection_panel.image.fblits([(element.get_drawable()) for element in self.tower_buttons_group])
        
        

    def load_towers_from_directory(self):
        tower_dir = "cctd/towers"
        tower_list = os.listdir(tower_dir)
        self.tower_directory_list = []
        
        for tower in tower_list:
            self.tower_directory_list.append(f"cctd/towers/{tower}")    
 
        
    def load_towers_on_panel(self):
        self.tower_buttons_group = []
        
        for idx, tower in enumerate(self.tower_directory_list):
           
            tower_obj = th.Tower(f"{tower}", 
                    f"{tower}/tower_data.json", 
                    pygame.image.load(f"{tower}/sprite.png").convert_alpha())
            
            # Calculate x and y coordinates
            x = 10 + (idx % 4) * 70  # num_columns is the number of towers you want in each row
            y = 10 + (idx // 4) * 70
            btn = glm.LiteImageButton(x, y, f"{tower}/cover.png")
            btn.tower = tower_obj
            
            self.tower_buttons_group.append(btn)
                    
    def select_tower_from_button(self, btn):
        self.tower_manager.set_selected_tower( btn.tower)
        
      
        
        
    
    def load_map(self):
        map_l = map_loader.Map_Loader()
        game_map = map_l.load_map()
        self.map_image, self.map_mask = game_map.load_map()
        self.map_waypoints = game_map.load_waypoint_data()
        
        return game_map
    
    