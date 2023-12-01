import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.utils import *
from ..libs.scenes import *
from ..libs.transitions import *

pygame.font.init()




class GUIText:
    def __init__(self, text, size, color, pos):
        self.text = text
        self.color = color
        self.pos = pos
        self.default_font = pygame.font.Font(os.path.join(current_dir, '..', '..', 'resources', 'constant', 'font.ttf'), size)
        self.stroke_color = (0, 0, 0)  # Default stroke color
        self.stroke_thickness = 1  # Default stroke thickness

    def normal_text(self, text):
        self.text = self.default_font.render(text, True, self.color)

    def stroke_text(self, text, thickness, color):
        self.stroke_thickness = thickness
        self.stroke_color = color

        # Create a surface for the actual text
        text_surface = self.default_font.render(text, True, self.color)

        # Create a surface for the text with stroke
        text_with_stroke = pygame.Surface((text_surface.get_width() + 2 * self.stroke_thickness,
                                           text_surface.get_height() + 2 * self.stroke_thickness), pygame.SRCALPHA)

        # Draw the stroke
        for dx in range(-self.stroke_thickness, self.stroke_thickness + 1):
            for dy in range(-self.stroke_thickness, self.stroke_thickness + 1):
                text_with_stroke.blit(text_surface, (dx + self.stroke_thickness, dy + self.stroke_thickness))

        # Fill the text surface with the stroke color
        text_with_stroke.fill(color + (255,), special_flags=pygame.BLEND_RGBA_MULT)

        self.text = text_with_stroke

    def draw(self, screen):
        screen.blit(self.text, self.pos)


class GUIElement:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class GameOverlay(GUIElement):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)
        self.healthText = None
        self.roundCounter = None



    def draw(self, surface):
        return super().draw(surface)
    











class Button:
    def __init__(self, x, y, image_off_path, image_on_path, on_click):
        self.image_off_path = image_off_path
        self.image_on_path = image_on_path
        self.on_click = on_click
        self.tween_target_pos = None
        self.tween_pos_duration = 0
        self.tween_pos_delay = 0
        self.tween_pos_function = None
        self.tween_pos_clock = 0
        self.state = "off"
        self.load_images()

        # Set the initial rect alignment to the center of the image
        self.rect = self.image_off.get_rect(center=(x, y))

    def load_images(self):
        self.image_off = load_image(self.image_off_path)
        self.image_on = load_image(self.image_on_path)

    def draw(self, screen):
        image = self.image_on if self.state == "on" else self.image_off
        screen.blit(image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = "on"

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.state == "on":
                self.state = "off"
                self.on_click()

    def tween_pos(self, target, duration_sec, delay_sec=0, tweening_function=pytweening.easeInOutQuad):
        self.tween_target_pos = target
        # Assuming 60 frames per second
        self.tween_pos_duration = int(duration_sec * 60)
        self.tween_pos_delay = int(delay_sec * 60)
        self.tween_pos_function = tweening_function
        self.tween_pos_clock = 0

    def update(self):
        if self.tween_target_pos is not None:
            self.update_tween('pos')

    def update_tween(self, tween_type):
        tween_target = getattr(self, f'tween_target_{tween_type}')
        tween_duration = getattr(self, f'tween_{tween_type}_duration', 0)
        tween_delay = getattr(self, f'tween_{tween_type}_delay', 0)
        tween_function = getattr(self, f'tween_{tween_type}_function', None)
        tween_clock = getattr(self, f'tween_{tween_type}_clock', 0)

        if tween_delay > 0:
            setattr(self, f'tween_{tween_type}_delay', tween_delay - 1)
        else:
            setattr(self, f'tween_{tween_type}_clock', tween_clock + 1)
            if tween_duration > 0 and tween_clock <= tween_duration:
                progress = tween_clock / tween_duration
                eased_progress = tween_function(progress)

                if tween_type == 'pos':
                    new_x = int(
                        self.rect.centerx + (tween_target[0] - self.rect.centerx) * eased_progress)
                    new_y = int(
                        self.rect.centery + (tween_target[1] - self.rect.centery) * eased_progress)

                    self.rect.center = (new_x, new_y)
            else:
                setattr(self, f'tween_target_{tween_type}', None)
                setattr(self, f'tween_{tween_type}_clock', 0)
                setattr(self, f'tween_{tween_type}_duration', 0)
                setattr(self, f'tween_{tween_type}_delay', 0)
                setattr(self, f'tween_{tween_type}_function', None)







