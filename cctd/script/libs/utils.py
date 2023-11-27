from pygame import QUIT
import pygame
from pytweening import easeInOutQuad


class TweenSprite:
    def __init__(self, start_pos, end_pos, image, duration, easing_function, delay=0):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.image = image
        self.duration = duration
        self.easing_function = easing_function
        self.delay = delay
        self.start_time = None  # Initialize start_time as None

    def update(self):
        if self.start_time is None:
            self.start_time = pygame.time.get_ticks() + int(self.delay * 1000)

        current_time = pygame.time.get_ticks()
        if current_time < self.start_time:
            return  # Delaying the start of the tween

        elapsed_time = current_time - self.start_time
        progress = min(elapsed_time / (self.duration * 1000), 1.0)

        # Use the provided easing function to calculate the interpolated position
        self.current_pos = (
            self.start_pos[0] + self.easing_function(
                progress) * (self.end_pos[0] - self.start_pos[0]),
            self.start_pos[1] + self.easing_function(
                progress) * (self.end_pos[1] - self.start_pos[1]),
        )

    def draw(self, screen):
        screen.blit(self.image, self.current_pos)


class TweenOpacity:
    def __init__(self, start_alpha, end_alpha, image, duration, easing_function, delay=0):
        self.start_alpha = start_alpha
        self.end_alpha = end_alpha
        self.image = image
        self.duration = duration
        self.easing_function = easing_function
        self.delay = delay
        self.start_time = None  # Initialize start_time as None

        # Set the initial alpha value to 0
        self.current_alpha = 0
        self.image.set_alpha(self.current_alpha)

    def start(self):
        # Start the tween by setting the start_time to the current time
        self.start_time = pygame.time.get_ticks() + int(self.delay * 1000)

    def update(self):
        if self.start_time is None:
            return  # The tween has not started yet

        current_time = pygame.time.get_ticks()
        if current_time < self.start_time:
            return  # Delaying the start of the tween

        elapsed_time = current_time - self.start_time
        progress = min(elapsed_time / (self.duration * 1000), 1.0)

        # Use the provided easing function to calculate the interpolated alpha
        self.current_alpha = int(
            self.start_alpha + self.easing_function(progress) * (self.end_alpha - self.start_alpha))
        self.image.set_alpha(self.current_alpha)

    def draw(self, screen):
        screen.blit(self.image, (0, 0))


def load_image(image_path):
    return pygame.image.load(image_path).convert_alpha()


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

    def tween_pos(self, target, duration_sec, delay_sec=0, tweening_function=easeInOutQuad):
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
