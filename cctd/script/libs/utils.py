import pygame, sys, os
from pytweening import easeInOutQuad

def load_image(image_path):
    return pygame.image.load(image_path).convert_alpha()

def quitGame():
        pygame.quit()
        sys.exit()


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

    def kill(self):
        del self



