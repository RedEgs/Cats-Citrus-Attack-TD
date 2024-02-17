import psutil, pygame, sys, os

import engine.libs.Utils as utils
import engine.libs.EntityService as EntityService
import engine.libs.SceneService as SceneService
import engine.libs.GuiService as GuiService
import engine.libs.TweenService as TweenService


class DebugService:
    def __init__(self, app, clock):
        self.app = app
        self.camera = self.app.get_camera()
        self.clock = clock




        i = 20
        j = self.camera.get_screen().get_size()[0]-40

        camera_info_title = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*1-3),
            f"Camera Service Info",
            16,
            (0, 0, 0),
            "left",
            True
        )
        
        self.camera_offset_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*2),
            f"Camera Offset: {str(self.camera.get_camera_offset())}",
            16,
            (0, 0, 0),
            "left",
        )
        
        self.camera_rect_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*3),
            f"Camera Bounds: [{str(self.camera.camera_bounds_rect.width)},{str(self.camera.camera_bounds_rect.height)}]",
            16,
            (0, 0, 0),
            "left",
        )
        
        self.zoom_amount_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*4),
            f"Zoom Amount: {self.camera.get_zoom()}",
            16,
            (0, 0, 0),
            "left",
        )
        
        self.surface_scale_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*5),
            f"Surface Scale (Resolution): {self.camera.get_display_output_size()}",
            16,
            (0, 0, 0),
            "left",
        )
        
        
        gui_service_title = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*7-3),
            f"GUI Service Info",
            16,
            (0, 0, 0),
            "left",
            True
        )
        
        self.gui_elements_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*8),
            f"Elements: Loading...",
            16,
            (0, 0, 0),
            "left",
        )
        
        self.gui_active_elements_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*9),
            f"Active Elements: Loading...",
            16,
            (0, 0, 0),
            "left",
        )
        
        self.gui_all_active_elements_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*10),
            f"All Active Elements: Loading...",
            16,
            (0, 0, 0),
            "left",
        )
         
         
         
         
         
        self.mouse_positions_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (i, i*13),
            f"Mouse Position (Screen | World): {pygame.mouse.get_pos()} | {pygame.mouse.get_pos()-self.camera.get_camera_offset()}",
            16,
            (0, 0, 0),
            "left",
        )
        
       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        self.fps_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (j, i*1),
            str(round(self.clock.get_fps(), 0)),
            16,
            (0, 0, 0),
            "right",
        )

        self.mem_usage_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN, self.camera, (j,i*2),"Mem Usage:", 16, (0, 0, 0), "right"
        )
        
        self.cpu_usage_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN, self.camera, (j,i*3),"CPU Usage:", 16, (0, 0, 0), "right"
        )
        

    def update(self):
        self.mem_usage = psutil.Process(os.getpid()).memory_info().rss / 1024**2
        self.cpu_usage = psutil.cpu_percent()


        
        self.mouse_positions_text.update_text(f"Mouse Position (Screen | World): {pygame.mouse.get_pos()} | {(pygame.mouse.get_pos()[0]/self.camera.camera_zoom_scale, pygame.mouse.get_pos()[1]/self.camera.camera_zoom_scale)}")
    
        
        self.camera_offset_text.update_text(f"Camera Offset: {str(self.camera.get_camera_offset())}")
        self.zoom_amount_text.update_text(f"Zoom Amount: {round(self.camera.get_zoom(), 4)}")
        self.surface_scale_text.update_text(f"Surface Scale (Resolution): {self.camera.get_display_output_size()}")


        self.gui_elements_text.update_text(f"Elements: {len(self.app.guis.ui_elements)}")
        self.gui_active_elements_text.update_text(f"Active Elements (Drawn): {len(self.app.guis.active_scene.ui_elements.sprites()) + len(self.app.guis.screen_ui_elements)}")
        self.gui_all_active_elements_text.update_text(f"All Active Elements (Drawn): {len(self.app.guis.active_scene.ui_elements.sprites()) + len(self.app.guis.screen_ui_elements) + len(self.app.guis.global_ui_elements)}")





        self.fps_text.update_text(f"FPS: {str(round(self.clock.get_fps()))}")
        self.mem_usage_text.update_text(f"Mem Usage: {round(self.mem_usage, 1)} MBs")
        self.cpu_usage_text.update_text(f"CPU Usage: {self.cpu_usage}%")