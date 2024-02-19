import psutil, pygame, sys, os
import threading, time



import engine.libs.Utils as utils
import engine.libs.EntityService as EntityService
import engine.libs.SceneService as SceneService
import engine.libs.GuiService as GuiService
import engine.libs.TweenService as TweenService

class DebugService:
    def __init__(self, app, clock):
        print("started init debug service")
        self.app = app
        self.camera = self.app.get_camera()
        self.clock = clock
        
        self.previous_fps = self.clock.get_fps()
        self.fps_high = self.previous_fps
        self.fps_low = 100
        self.current_fps = 0
        
        self.cpu_usage = "Loading"


        self.font_size = 12
        i = 20
        j = self.camera.get_screen().get_size()[0]

        self.start_debug_info()



        camera_info_title = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*1-3),
            f"Camera Service Info",
            self.font_size,
            (0, 0, 0),
            "left",
            True
        )
        
        self.camera_offset_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*2),
            f"Camera Offset: {str(self.camera.get_camera_offset())}",
            self.font_size,
            (0, 0, 0),
            "left",
        )
        
        self.camera_rect_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*3),
            f"Camera Bounds: [{str(self.camera.camera_bounds_rect.width)},{str(self.camera.camera_bounds_rect.height)}]",
            self.font_size,
            (0, 0, 0),
            "left",
        )
        
        self.zoom_amount_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*4),
            f"Zoom Amount: {self.camera.get_zoom()}",
            self.font_size,
            (0, 0, 0),
            "left",
        )
        
        self.surface_scale_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*5),
            f"Surface Scale (Resolution): {self.camera.get_display_output_size()}",
            self.font_size,
            (0, 0, 0),
            "left",
        )
        
        
        gui_service_title = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*7-3),
            f"GUI Service Info",
            self.font_size,
            (0, 0, 0),
            "left",
            True
        )
        
        self.gui_elements_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*8),
            f"Elements: Loading...",
            self.font_size,
            (0, 0, 0),
            "left",
        )
        
        self.gui_active_elements_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*9),
            f"Active Elements: Loading...",
            self.font_size,
            (0, 0, 0),
            "left",
        )
        
        self.gui_all_active_elements_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*10),
            f"All Active Elements: Loading...",
            self.font_size,
            (0, 0, 0),
            "left",
        )
         
        self.mouse_positions_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*13),
            f"Mouse Position (Screen | World): {pygame.mouse.get_pos()} | {pygame.mouse.get_pos()-self.camera.get_camera_offset()}",
            self.font_size,
            (0, 0, 0),
            "left",
        )
         
        self.fps_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (j, i*1),
            str(round(self.clock.get_fps(), 0)),
            self.font_size,
            (0, 0, 0),
            "right",
        )

        self.mem_usage_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN, self.camera, (j,i*2),"Mem Usage:", self.font_size, (0, 0, 0), "right"
        )
        
        self.cpu_usage_text = GuiService.FreeTextElement(
            GuiService.GuiSpaces.SCREEN, self.camera, (j,i*3),"CPU Usage:", self.font_size, (0, 0, 0), "right"
        )
        
    def start_debug_info(self):
        pass
        #fps_counter_thread = threading.Thread(target=self.debug_fps_info).start()
        #cpu_counter_thread = threading.Thread(target=self.debug_cpu_info).start()
    
    
    def debug_fps_info(self):  
        self.current_fps = self.clock.get_fps()
        
        if self.current_fps > self.fps_high:
            self.fps_high = self.current_fps
                
        if self.current_fps < self.fps_low and self.current_fps != 0:
            self.fps_low = self.current_fps
            #print(f"Current: {round(self.current_fps)} | High: {round(self.fps_high)} | Low: {round(self.fps_low)}")
            #print(f"Current: {round(self.current_fps)} | High: {round(self.fps_high)} | Low: {round(self.fps_low)}")
            #print(f"Current: {round(self.current_fps)} | High: {round(self.fps_high)} | Low: {round(self.fps_low)}")
            
        
    def debug_cpu_info(self):
        pid = os.getpid()
        process = psutil.Process(pid)
        
        while True:            
            self.cpu_usage = round(process.cpu_percent(interval=10) - 100.0)
                
            #print(f"Current: {round(self.current_fps)} | High: {round(self.fps_high)} | Low: {round(self.fps_low)}")
    
        
        
        
        
        
                


                    
            
            
                

            
    
        
           
        
        
        

    def update(self):
        self.debug_fps_info()
        self.mem_usage = psutil.Process(os.getpid()).memory_info().rss / 1024**2
        
        self.mouse_positions_text.update_text(f"Mouse Position (Screen | World): {pygame.mouse.get_pos()} | {(pygame.mouse.get_pos()[0]/self.camera.camera_zoom_scale, pygame.mouse.get_pos()[1]/self.camera.camera_zoom_scale)}")
    
        
        self.camera_offset_text.update_text(f"Camera Offset: {str(self.camera.get_camera_offset())}")
        self.zoom_amount_text.update_text(f"Zoom Amount: {round(self.camera.get_zoom(), 4)}")
        self.surface_scale_text.update_text(f"Surface Scale (Resolution): {self.camera.get_display_output_size()}")


        self.gui_elements_text.update_text(f"Elements: {len(self.app.guis.ui_elements)}")
        self.gui_active_elements_text.update_text(f"Active Elements (Drawn): {len(self.app.guis.active_scene.ui_elements.sprites()) + len(self.app.guis.screen_ui_elements)}")
        self.gui_all_active_elements_text.update_text(f"All Active Elements (Drawn): {len(self.app.guis.active_scene.ui_elements.sprites()) + len(self.app.guis.screen_ui_elements) + len(self.app.guis.global_ui_elements)}")


        self.fps_text.update_text(f"Current: {round(self.current_fps)} | High: {round(self.fps_high)} | Low: {round(self.fps_low)}")
        self.mem_usage_text.update_text(f"Mem Usage: {round(self.mem_usage, 1)} MBs")
        self.cpu_usage_text.update_text(f"CPU Usage: {self.cpu_usage}%")
