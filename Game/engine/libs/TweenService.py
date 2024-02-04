import pygame, pytweening, json, os, sys

from typing import Callable
from dataclasses import dataclass

import engine.libs.Utils as Utils

class TweenService():
    tweens = []
    active_tweens = []

    @classmethod
    def add_tween(cls, tween):
        cls.tweens.append(tween)

    @classmethod
    def activate_tween(cls, tween):
        cls.active_tweens.append(tween)

    @classmethod
    def deactivate_tween(cls, tween):
        cls.active_tweens.pop(Utils.get_item_index(tween, cls.active_tweens))
        del tween

    @classmethod
    def update(cls):
        for tween in cls.active_tweens:
            #print(tween.get_output())
            tween.update()
    
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
        self.reversed = False

        self.start_time = None
        self.current_value = self.start_value
        self.is_finished = False  # Flag to track whether the tween has finished
        self.reverse_on_finish = False  # Flag to determine whether to reverse on finish

        TweenService.add_tween(self)


    def start(self, reverse_on_finish=False, dont_finish_tween=False):
        self.reverse_on_finish = reverse_on_finish
        self.dont_finish_tween = dont_finish_tween

        if self.delay <= 0 or self.delay is None:
            self.start_time = pygame.time.get_ticks()
            TweenService.activate_tween(self)
        else:
            self.start_time = pygame.time.get_ticks() + self.delay
            TweenService.activate_tween(self)

    def reverse(self):
        self.reversed = True
        if not self.is_finished:
            if not self.reversed:

                # Reverse the animation manually
                self.reverse_animation()

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
                        if self.dont_finish_tween == True:
                            pass
                        else:
                            self.is_finished = True  # Mark the tween as finished
                            TweenService.deactivate_tween(self)

                        if self.reverse_on_finish:
                            # Reverse the animation on finish
                            self.reverse_animation()

    def reverse_animation(self):
        # Swap start and end values to reverse the animation
        self.start_value, self.end_value = self.end_value, self.start_value
        self.start_time = pygame.time.get_ticks()  # Reset start time for the reversed animation
        self.is_finished = False  # Reset finished flag for the reversed animation

    def is_reversed(self):
        return self.start_value == self.end_value    

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
    def __init__(self, tween_data: TweenData):
        self.TweenData = tween_data

        self.start_value = self.TweenData.start_value
        self.end_value = self.TweenData.end_value
        self.duration = self.TweenData.duration * 1000
        self.delay = self.TweenData.delay * 1000
        self.easing_function = self.TweenData.easing_function

        self.start_time = None
        self.current_value = self.start_value
        self.is_finished = False  # Flag to track whether the tween has finished
        self.reverse_on_finish = False  # Flag to determine whether to reverse on finish
        self.reversed = False

        TweenService.add_tween(self)


    def start(self, reverse_on_finish=False, dont_finish_tween=False):
        self.reverse_on_finish = reverse_on_finish
        self.dont_finish_tween = dont_finish_tween

        if self.delay <= 0 or self.delay is None:
            self.start_time = pygame.time.get_ticks()
            TweenService.activate_tween(self)
        else:
            self.start_time = pygame.time.get_ticks() + self.delay
            TweenService.activate_tween(self)

    def reverse(self, dont_finish_reverse=True):
        self.reversed = True
        if not self.is_finished:
            # Reverse the animation manually
            #if not self.reversed:
                self.reverse_animation(dont_finish_reverse)

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
                    self.current_value = self.start_value + self.easing_function(progress) * (self.end_value - self.start_value)

                    if progress >= 1.0:
                        if self.dont_finish_tween == True:
                            pass
                        else:
                            self.is_finished = True  # Mark the tween as finished
                            TweenService.deactivate_tween(self)

                        if self.reverse_on_finish:
                            # Reverse the animation on finish
                            self.reverse_animation()

    def reverse_animation(self, finish_reverse=True):
        # Swap start and end values to reverse the animation
        self.start_value, self.end_value = self.end_value, self.start_value
        self.start_time = pygame.time.get_ticks()  # Reset start time for the reversed animation
        self.is_finished = finish_reverse  # Reset finished flag for the reversed animation

    def is_reversed(self):
        return self.start_value == self.end_value    

    def get_output(self):
        return self.current_value

    def check_finished(self):
        return self.is_finished

    def kill(self):
        print("deleted: " + str(self))
        del self