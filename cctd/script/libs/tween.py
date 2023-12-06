import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from typing import Callable
from dataclasses import dataclass

from ..libs.utils import *
from ..libs.scenes import *
from ..libs.transitions import *

class TweenDirector():
    def __init__(self):
        self.tweens = []

    def update(self, callbacks=None):
        self.callbacks = callbacks if callbacks is not None else []

        for tween in self.tweens:
            if tween.check_finished():
                self.tweens.pop(self.tweens.index(tween))

            tween.update()

            if callbacks is not None:
                for callback in callbacks:
                    callback

                

    def get_tweens(self):
        return self.tweens







@dataclass
class TweenDataVector2():
    start_value: (int, int)
    end_value: (int, int)
    duration: float
    delay: float
    easing_function: Callable[[float], float] = pytweening.linear
        
class TweenDataVector2:
    def __init__(self, start_value, end_value, duration, delay, easing_function):
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.delay = delay
        self.easing_function = easing_function

class TweenVector2:
    def __init__(self, tween_data: TweenDataVector2, tween_director):
        self.tween_director = tween_director
        self.TweenData = tween_data

        self.start_value = self.TweenData.start_value
        self.end_value = self.TweenData.end_value
        self.duration = self.TweenData.duration * 1000
        self.delay = self.TweenData.delay * 1000
        self.easing_function = self.TweenData.easing_function

        self.start_time = None
        self.current_value = self.start_value
        self.is_finished = False  # Flag to track whether the tween has finished

        self.tween_director.get_tweens().append(self)

    def start(self):
        if self.delay <= 0 or self.delay is None:
            self.start_time = pygame.time.get_ticks()
        else:
            self.start_time = pygame.time.get_ticks() + self.delay

    def update(self):
        if not self.is_finished:  # Only update if the tween is not finished
            if self.start_time is None:
                pass
            else:
                current_time = pygame.time.get_ticks()

                elapsed_time = current_time - self.start_time

                if elapsed_time >= self.delay:
                    progress = min((elapsed_time - self.delay) / self.duration, 1.0)

                    # Use the provided easing function to calculate the interpolated value
                    self.current_value = (
                        self.start_value[0] + self.easing_function(progress) * (self.end_value[0] - self.start_value[0]),
                        self.start_value[1] + self.easing_function(progress) * (self.end_value[1] - self.start_value[1]),
                    )
                    if progress >= 1.0:
                        self.is_finished = True  # Mark the tween as finished

    def get_output(self):
        return self.current_value

    def check_finished(self):
        return self.is_finished

    def kill(self):
        del self

@dataclass
class TweenData():
    start_value: float
    end_value: float
    duration: int
    delay: int
    easing_function: Callable[[float], float] = pytweening.linear

class Tween:
    def __init__(self, tween_data: TweenData, tween_director):
        self.TweenData = tween_data
        self.tween_director = tween_director

        self.start_value = self.TweenData.start_value
        self.end_value = self.TweenData.end_value
        self.duration = self.TweenData.duration * 1000
        self.delay = self.TweenData.delay * 1000
        self.easing_function = self.TweenData.easing_function

        self.start_time = None
        self.current_value = self.start_value
        self.is_finished = False  # Flag to track whether the tween has finished
        self.delay_completed = False  # Flag to track whether the delay has been completed

        self.tween_director.get_tweens().append(self)

    def start(self):
        if self.delay <= 0 or self.delay is None:
            self.start_time = pygame.time.get_ticks()
        else:
            self.start_time = pygame.time.get_ticks()

    def update(self):
        if not self.is_finished:  # Only update if the tween is not finished
            if self.start_time is None:
                pass
            else:
                current_time = pygame.time.get_ticks()

                elapsed_time = current_time - self.start_time

                if elapsed_time >= self.delay and not self.delay_completed:
                    self.delay_completed = True
                    self.start_time = current_time

                if self.delay_completed:
                    progress = min((elapsed_time - self.delay) / self.duration, 1.0)

                    # Use the provided easing function to calculate the interpolated value
                    self.current_value = self.start_value + self.easing_function(progress) * (self.end_value - self.start_value)

                    if progress >= 1.0:
                        self.is_finished = True  # Mark the tween as finished

    def get_output(self):
        return self.current_value

    def check_finished(self):
        return self.is_finished

    def kill(self):
        del self

#SECTION - Presets Data

opacity_fade_in_data = TweenData(1, 255, 1, 0, pytweening.easeInOutQuad)


#SECTION - Presets Functions
