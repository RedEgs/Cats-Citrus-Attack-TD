import pytweening, pygame, pydantic, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from typing import Callable
from dataclasses import dataclass

from ..libs.utils import *
from ..libs.scenes import *
from ..libs.transitions import *

@dataclass
class TweenDataVector2():
    start_value: (int, int)
    end_value: (int, int)
    duration: float
    delay: float
    easing_function: Callable[[float], float] = pytweening.linear
        
class TweenVector2:
    def __init__(self, tween_data: TweenDataVector2):
        self.TweenData = tween_data

        self.start_value = self.TweenData.start_value 
        self.end_value = self.TweenData.end_value
        self.duration = self.TweenData.duration * 1000
        self.delay = self.TweenData.delay * 1000
        self.easing_function = self.TweenData.easing_function

        self.start_time = None
        self.current_value = self.start_value

    def start(self):
        if self.delay <= 0 or self.delay is None or self.start_time is None:
            self.start_time = pygame.time.get_ticks()
        else:
            self.start_time = pygame.time.get_ticks() + self.delay


    def update(self):
        if self.start_time is None:
            pass
        else:
            current_time = pygame.time.get_ticks()

            elapsed_time = current_time - self.start_time
            print(min(elapsed_time / self.duration, 1.0))
            progress = min(elapsed_time / self.duration, 1.0)
            
            self.current_value = (
                self.start_value[0] + self.easing_function(
                    progress) * (self.end_value[0] - self.start_value[0]),
                
                self.start_value[1] + self.easing_function(
                    progress) * (self.end_value[1] - self.start_value[1]),
            )

            # Use the provided easing function to calculate the interpolated value
            self.current_value = (
                self.start_value[0] + self.easing_function(progress) * (self.end_value[0] - self.start_value[0]),
                self.start_value[1] + self.easing_function(progress) * (self.end_value[1] - self.start_value[1]),
            )

    def get_output(self):
        return self.current_value

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
    def __init__(self, tween_data: TweenData):
        self.TweenData = tween_data

        self.start_value = self.TweenData.start_value 
        self.end_value = self.TweenData.end_value
        self.duration = self.TweenData.duration * 1000
        self.delay = self.TweenData.delay * 1000
        self.easing_function = self.TweenData.easing_function

        self.start_time = None
        self.current_value = self.start_value

    def start(self):
        if self.delay <= 0 or self.delay is None or self.start_time is None:
            self.start_time = pygame.time.get_ticks()
        else:
            self.start_time = pygame.time.get_ticks() + self.delay


    def update(self):
        if self.start_time is None:
            pass
        else:
            current_time = pygame.time.get_ticks()

            elapsed_time = current_time - self.start_time
            print(min(elapsed_time / self.duration, 1.0))
            progress = min(elapsed_time / self.duration, 1.0)
            

            # Use the provided easing function to calculate the interpolated value
            self.current_value = self.start_value + self.easing_function(progress) * (self.end_value - self.start_value)

    def get_output(self):
        return self.current_value

    def kill(self):
        del self
        
        