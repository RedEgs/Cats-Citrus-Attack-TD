from engine.libs.Services import Service
import psutil, pygame, sys, os
import threading, time


import engine.libs.Utils as utils
import engine.libs.EntityService as EntityService
import engine.libs.SceneService as SceneService
import engine.libs.GuiService as GuiService
import engine.libs.TweenService as TweenService

class DebugService(Service):
    def __init__(self, app, clock):
        self.app = app
        self.camera = self.app.get_camera()
        self.clock = clock
        
        self.hidden_list = []
        self.debug_hidden = False
        
        self.previous_fps = self.clock.get_fps()
        self.fps_high = self.previous_fps
        self.fps_low = 100
        self.current_fps = 0
        
        self.cpu_usage = "Loading"


        self.font_size = 12
        i = 20
        j = self.camera.get_screen().get_size()[0]-20

        self.start_debug_info()

        camera_info_title = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*1-3),
            f"Camera Service Info",
            self.font_size,
            (250, 250, 250),
            "left",
            True
        )
        
        self.camera_offset_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*2),
            f"Camera Offset: {str(self.camera.get_camera_offset())}",
            self.font_size,
            (250, 250, 250),
            "left",
        )
        
        self.camera_rect_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*3),
            f"Camera Bounds: [{str(self.camera.camera_bounds_rect.width)},{str(self.camera.camera_bounds_rect.height)}]",
            self.font_size,
            (250, 250, 250),
            "left",
        )
        
        self.zoom_amount_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*4),
            f"Zoom Amount: {self.camera.get_zoom()}",
            self.font_size,
            (250, 250, 250),
            "left",
        )
        
        self.surface_scale_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*5),
            f"Surface Scale (Resolution): {self.camera.get_display_output_size()}",
            self.font_size,
            (250, 250, 250),
            "left",
        )
        
        
        gui_service_title = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*7-3),
            f"GUI Service Info",
            self.font_size,
            (250, 250, 250),
            "left",
            True
        )
        
        self.gui_elements_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*8),
            f"Elements: Loading...",
            self.font_size,
            (250, 250, 250),
            "left",
        )
        
        self.gui_active_elements_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*9),
            f"Active Elements: Loading...",
            self.font_size,
            (250, 250, 250),
            "left",
        )
        
        self.gui_all_active_elements_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*10),
            f"All Active Elements: Loading...",
            self.font_size,
            (250, 250, 250),
            "left",
        )
         
        self.mouse_positions_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*13),
            f"Mouse Position (Screen | World): {pygame.mouse.get_pos()} | {pygame.mouse.get_pos()-self.camera.get_camera_offset()}",
            self.font_size,
            (250, 250, 250),
            "left",
        )
              
        performance_stats_title = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (j, i*1-3),
            f"Performance Stats Info",
            self.font_size,
            (250, 250, 250),
            "right",
            True
        )

        self.fps_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (j, i*2),
            str(round(self.clock.get_fps(), 0)),
            self.font_size,
            (250, 250, 250),
            "right",
        )

        self.mem_usage_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN, self.camera, (j,i*3),"Mem Usage:", self.font_size, (250, 250, 250), "right"
        )
        
        self.cpu_usage_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN, self.camera, (j,i*4),"CPU Usage:", self.font_size, (250, 250, 250), "right"
        )
        
    def start_debug_info(self):
        #fps_counter_thread = threading.Thread(target=self.debug_fps_info).start()
        cpu_counter_thread = threading.Thread(target=self.debug_cpu_info).start()
    
       #print(f"Current: {round(self.current_fps)} | High: {round(self.fps_high)} | Low: {round(self.fps_low)}")
            #print(f"Current: {round(self.current_fps)} | High: {round(self.fps_high)} | Low: {round(self.fps_low)}")
            
        
    def debug_cpu_info(self):
        pid = os.getpid()
        process = psutil.Process(pid)
        
        while True:     
            #time.sleep(0.5)
            self.mem_usage = psutil.Process(os.getpid()).memory_info().rss / 1024**2      
            cpu_usage = round(process.cpu_percent(interval=.5))

            if cpu_usage > 100.0:
                self.cpu_usage = cpu_usage - 100.0
            else:
                self.cpu_usage = cpu_usage
                
            #print(f"Current: {round(self.current_fps)} | High: {round(self.fps_high)} | Low: {round(self.fps_low)}")
    
    def debug_fps_info(self):  
        self.current_fps = self.clock.get_fps()
        
        if self.current_fps > self.fps_high:
            self.fps_high = self.current_fps
                
        if self.current_fps < self.fps_low and self.current_fps != 0:
            self.fps_low = self.current_fps
            
        print(f"Current: {round(self.current_fps)} | High: {round(self.fps_high)} | Low: {round(self.fps_low)}")
         
    
    def update(self):
        self.debug_fps_info()
        
        
        self.mouse_positions_text.update_text(f"Mouse Position (Screen | World): {pygame.mouse.get_pos()} | {(pygame.mouse.get_pos()[0]+self.camera.get_camera_offset()[0]/self.camera.camera_zoom_scale, pygame.mouse.get_pos()[1]+self.camera.get_camera_offset()[1]/self.camera.camera_zoom_scale)}")
    
        
        self.camera_offset_text.update_text(f"Camera Offset: {(self.camera.camera_offset[0] + int(self.camera.screen_w) / 2, self.camera.camera_offset[1] + int(self.camera.screen_h) / 2)}")
        self.zoom_amount_text.update_text(f"Zoom Amount: {round(self.camera.get_zoom(), 4)}")
        self.surface_scale_text.update_text(f"Surface Scale (Resolution): {self.camera.get_display_output_size()}")


        self.gui_elements_text.update_text(f"Elements: {len(self.app.gui_service.ui_elements)}")
        self.gui_active_elements_text.update_text(f"Active Elements (Drawn): {len(self.app.gui_service.active_scene.ui_elements.sprites()) + len(self.app.gui_service.screen_ui_elements)}")
        self.gui_all_active_elements_text.update_text(f"All Active Elements (Drawn): {len(self.app.gui_service.active_scene.ui_elements.sprites()) + len(self.app.gui_service.screen_ui_elements) + len(self.app.gui_service.global_ui_elements)}")


        self.fps_text.update_text(f"Current: {round(self.current_fps)} | High: {round(self.fps_high)} | Low: {round(self.fps_low)}")
        self.mem_usage_text.update_text(f"Mem Usage: {round(self.mem_usage, 1)} MBs")
        self.cpu_usage_text.update_text(f"CPU Usage: {self.cpu_usage}%")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                self.hide_debug_info()

    def hide_debug_info(self):
        if self.debug_hidden == False:
            for element in self.app.gui_service.global_ui_elements:
                element.hide()
                self.hidden_list.append(element)

            self.debug_hidden = True

        else: 
            for element in self.hidden_list:
                element.unhide()
                
            self.hidden_list.clear()
            self.debug_hidden = False
        