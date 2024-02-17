import psutil, pytweening, pygame, sys, os


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

        self.camera_offset_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (20, 20),
            f"Camera Offset: {str(self.camera.get_camera_offset())}",
            14,
            (0, 0, 0),
            "left",
        )
        
        self.camera_rect_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (20, 40),
            f"Camera Bounds: [{str(self.camera.camera_bounds_rect.width)},{str(self.camera.camera_bounds_rect.height)}]",
            14,
            (0, 0, 0),
            "left",
        )
        
        self.zoom_amount_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (20, 60),
            f"Zoom Amount: {self.camera.get_zoom()}",
            14,
            (0, 0, 0),
            "left",
        )
        
        self.surface_scale_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (20, 80),
            f"Surface Scale (Resolution): {self.camera.get_display_output_size()}",
            14,
            (0, 0, 0),
            "left",
        )
        
        
        self.fps_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN,
            self.camera,
            (20, 120),
            str(round(self.clock.get_fps(), 0)),
            14,
            (0, 0, 0),
            "left",
        )

        self.mem_usage = psutil.Process(os.getpid()).memory_info().rss / 1024**2
        self.mem_usage_text = GuiService.TextElement(
            GuiService.GuiSpaces.SCREEN, self.camera, (20,140), ("Mem Usage: "), 14, (0, 0, 0), "left"
        )


    def update(self):
        self.mem_usage = psutil.Process(os.getpid()).memory_info().rss / 1024**2
        
        self.camera_offset_text.update_text(f"Camera Offset: {str(self.camera.get_camera_offset())}")
        self.zoom_amount_text.update_text(f"Zoom Amount: {round(self.camera.get_zoom(), 4)}")
        self.surface_scale_text.update_text(f"Surface Scale (Resolution): {self.camera.get_display_output_size()}")


        self.fps_text.update_text(f"FPS: {str(round(self.clock.get_fps()))}")
        self.mem_usage_text.update_text(f"Mem Usage : {round(self.mem_usage, 1)} MBs")
