from engine.libs.Services import Service
import pygame, pytweening, json, os, sys


class TweenService(Service):
    tweens = []
    active_tweens = []

    @classmethod
    def add_tween(cls, tween):
        if not tween in cls.tweens:
            cls.tweens.append(tween)

    @classmethod
    def start_tween(cls, tween):
        if not tween in cls.active_tweens:
            cls.active_tweens.append(tween)

    @classmethod
    def stop_tween(cls, tween):
        cls.active_tweens.remove(tween)
        
    @classmethod
    def kill_tween(cls, tween):
        try:
            cls.active_tweens.remove(tween)
        except: pass
        try:
            cls.tweens.remove(tween)
        except: pass
        del tween
    
    @classmethod
    def update(cls, delta_time):
        active_tween = [tween.update(delta_time) for tween in cls.active_tweens]

class Tween():
    from typing import Callable, Union
    
    def __init__(self, pos_1: Union[int, pygame.Vector2], 
                 pos_2: Union[int, pygame.Vector2], 
                 time: float = 1, 
                 easing_type: Callable[[float], float] = pytweening.linear,
                 **settings):
        
        self.pos_1 = pos_1
        self.pos_2 = pos_2
    
        self.time = time
        self.easing_type = easing_type
        
        self.t_settings = settings
        
        self.progress = 0.0
        self._finished = False
        self._started = False
        self._tween_factor = 0
        
        self.load_settings()
        
        if type(self.pos_1) is pygame.Vector2 and type(self.pos_2) is pygame.Vector2:
            self.output_pos = pytweening.getPointOnLine(self.pos_1[0], self.pos_1[1],
                                                        self.pos_2[0], self.pos_2[1],
                                                        self._tween_factor)
        if type(self.pos_1) is int and type(self.pos_2) is int:
            self.output_pos = pytweening.getPointOnLine(self.pos_1, self.pos_1,
                                                        self.pos_2, self.pos_2,
                                                        self._tween_factor)
        
        TweenService.add_tween(self)
        
    def load_settings(self):
        """
        1 - On start callback
        2 - On stop callback
        3 - Start delay
        4 - Reverse on finish 
        """
        self.callback_1 = None
        self.callback_2 = None
        self.delay = 0
        self.reverse_on_finish = False
        
        self.reverse_once = False
        self._finished_reverse = False
        
        print(self.t_settings)
        for setting, value in self.t_settings.items():
            if setting == "on_start":
                self.callback_1 = value
            elif setting == "on_stop":
                self.callback_2 = value
            elif setting == "delay":
                self.delay = value
            elif setting == "reverse":
                self.reverse_on_finish = True
            elif setting == "reverse_once":
                self.reverse_once = True
                 
    def start(self):
        self.on_start()
        
        self._start_time = pygame.time.get_ticks()
        self._started = True
        
        if type(self.pos_1) is pygame.Vector2 and type(self.pos_2) is pygame.Vector2:
            self.output_pos = pytweening.getPointOnLine(self.pos_1[0], self.pos_1[1],
                                                        self.pos_2[0], self.pos_2[1],
                                                        self._tween_factor)
        if type(self.pos_1) is int and type(self.pos_2) is int:
            self.output_pos = pytweening.getPointOnLine(self.pos_1, self.pos_1,
                                                        self.pos_2, self.pos_2,
                                                        self._tween_factor)
        
        TweenService.start_tween(self)
        
    def stop(self):
        self._started = False
        self._finished = True
        

        if self.reverse_on_finish:
            if self.reverse_once and not self._finished_reverse:
                self.reverse()
                self._finished_reverse = True
            
            self.reverse()
            
            
        
        TweenService.stop_tween(self)
        self.on_stop()
        

       
    def reverse(self):
        self.progress = 0
        self._finished = False
        self._started = False
        self._tween_factor = 0
        
        temp_pos = self.pos_1
        self.pos_1 = self.pos_2
        self.pos_2 = temp_pos
            
        self.start()
       
       
    def kill(self):
        TweenService.kill_tween(self)    
          
    def update(self, delta_time):
        if self._start_time + (self.delay * 1000) <= pygame.time.get_ticks():
            if self._started and self.progress <= 1.0:
                self.progress += delta_time / self.time
                self._tween_factor = self.easing_type(self.progress)
                    
                if type(self.pos_1) is pygame.Vector2 and type(self.pos_2) is pygame.Vector2:
                    self.output_pos = pytweening.getPointOnLine(self.pos_1[0], self.pos_1[1],
                                                                self.pos_2[0], self.pos_2[1],
                                                                self._tween_factor)
                if type(self.pos_1) is int and type(self.pos_2) is int:
                    self.output_pos = pytweening.getPointOnLine(self.pos_1, self.pos_1,
                                                                self.pos_2, self.pos_2,
                                                                self._tween_factor)
            
            if self.progress >= 1.0 and not self._finished:
                self.stop()
                
       
    def on_start(self):
        if self.callback_1 is not None and not self._started:
            self.callback_1()
        
    def on_stop(self):
        if self.callback_2 is not None:
            
            self.callback_2()
          
    def check_finished(self):
        return self._finished

    def check_started(self):
        return self._started
    
    def get_start_time(self):
        return self._start_time
    
    def get_progress(self):
        return self.progress
    
    def get_output(self):
        if  type(self.pos_1) is pygame.Vector2 and type(self.pos_2) is pygame.Vector2:
            return pygame.Vector2(self.output_pos)
        if type(self.pos_1) is int and type(self.pos_2) is int:
            return self.output_pos[0]

        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

# @dataclass
# class TweenDataVector2():
#     start_value: (int, int)
#     end_value: (int, int)
#     duration: float
#     delay: float
#     easing_function: Callable[[float], float] = pytweening.linear

# class TweenVector2:
#     def __init__(self, tween_data: TweenDataVector2):
#         self.TweenData = tween_data

#         self.start_value = self.TweenData.start_value
#         self.end_value = self.TweenData.end_value
#         self.duration = self.TweenData.duration * 1000
#         self.delay = self.TweenData.delay * 1000
#         self.easing_function = self.TweenData.easing_function
#         self.reversed = False

#         self.start_time = None
#         self.current_value = self.start_value
#         self.is_finished = False  # Flag to track whether the tween has finished
#         self.reverse_on_finish = False  # Flag to determine whether to reverse on finish

#         TweenService.add_tween(self)


#     def start(self, reverse_on_finish=False, dont_finish_tween=False):
#         self.reverse_on_finish = reverse_on_finish
#         self.dont_finish_tween = dont_finish_tween

#         if self.delay <= 0 or self.delay is None:
#             self.start_time = pygame.time.get_ticks()
#             TweenService.activate_tween(self)
#         else:
#             self.start_time = pygame.time.get_ticks() + self.delay
#             TweenService.activate_tween(self)

#     def reverse(self):
#         self.reversed = True
#         if not self.is_finished:
#             if not self.reversed:

#                 # Reverse the animation manually
#                 self.reverse_animation()

#     def update(self):
#         if not self.is_finished:  # Only update if the tween is not finished
#             if self.start_time is None:
#                 pass
#             else:
#                 current_time = pygame.time.get_ticks()

#                 elapsed_time = current_time - self.start_time

#                 if elapsed_time >= self.delay:
#                     progress = min((elapsed_time - self.delay) / self.duration, 1.0)

#                     # Use the provided easing function to calculate the interpolated value
#                     self.current_value = (
#                         self.start_value[0] + self.easing_function(progress) * (self.end_value[0] - self.start_value[0]),
#                         self.start_value[1] + self.easing_function(progress) * (self.end_value[1] - self.start_value[1]),
#                     )

#                     if progress >= 1.0:
#                         if self.dont_finish_tween == True:
#                             pass
#                         else:
#                             self.is_finished = True  # Mark the tween as finished
#                             TweenService.deactivate_tween(self)

#                         if self.reverse_on_finish:
#                             # Reverse the animation on finish
#                             self.reverse_animation()

#     def reverse_animation(self):
#         # Swap start and end values to reverse the animation
#         self.start_value, self.end_value = self.end_value, self.start_value
#         self.start_time = pygame.time.get_ticks()  # Reset start time for the reversed animation
#         self.is_finished = False  # Reset finished flag for the reversed animation

#     def is_reversed(self):
#         return self.start_value == self.end_value    

#     def get_output(self):
#         return self.current_value

#     def check_finished(self):
#         return self.is_finished

#     def kill(self):
#         del self

# @dataclass
# class TweenData():
#     start_value: float
#     end_value: float
#     duration: int
#     delay: int
#     easing_function: Callable[[float], float] = pytweening.linear

# class Tween:
#     def __init__(self, tween_data: TweenData):
#         self.TweenData = tween_data

#         self.start_value = self.TweenData.start_value
#         self.end_value = self.TweenData.end_value
#         self.duration = self.TweenData.duration * 1000
#         self.delay = self.TweenData.delay * 1000
#         self.easing_function = self.TweenData.easing_function

#         self.start_time = None
#         self.current_value = self.start_value
#         self.is_finished = False  # Flag to track whether the tween has finished
#         self.reverse_on_finish = False  # Flag to determine whether to reverse on finish
#         self.reversed = False

#         TweenService.add_tween(self)


#     def start(self, reverse_on_finish=False, dont_finish_tween=False):
#         self.reverse_on_finish = reverse_on_finish
#         self.dont_finish_tween = dont_finish_tween

#         if self.delay <= 0 or self.delay is None:
#             self.start_time = pygame.time.get_ticks()
#             TweenService.activate_tween(self)
#         else:
#             self.start_time = pygame.time.get_ticks() + self.delay
#             TweenService.activate_tween(self)

#     def reverse(self, dont_finish_reverse=True):
#         self.reversed = True
#         if not self.is_finished:
#             # Reverse the animation manually
#             #if not self.reversed:
#                 self.reverse_animation(dont_finish_reverse)

#     def update(self):
#         if not self.is_finished:  # Only update if the tween is not finished
#             if self.start_time is None:
#                 pass
#             else:
#                 current_time = pygame.time.get_ticks()

#                 elapsed_time = current_time - self.start_time

#                 if elapsed_time >= self.delay:
#                     progress = min((elapsed_time - self.delay) / self.duration, 1.0)

#                     # Use the provided easing function to calculate the interpolated value
#                     self.current_value = self.start_value + self.easing_function(progress) * (self.end_value - self.start_value)

#                     if progress >= 1.0:
#                         if self.dont_finish_tween == True:
#                             pass
#                         else:
#                             self.is_finished = True  # Mark the tween as finished
#                             TweenService.deactivate_tween(self)

#                         if self.reverse_on_finish:
#                             # Reverse the animation on finish
#                             self.reverse_animation()

#     def reverse_animation(self, finish_reverse=True):
#         # Swap start and end values to reverse the animation
#         self.start_value, self.end_value = self.end_value, self.start_value
#         self.start_time = pygame.time.get_ticks()  # Reset start time for the reversed animation
#         self.is_finished = finish_reverse  # Reset finished flag for the reversed animation

#     def is_reversed(self):
#         return self.start_value == self.end_value    

#     def get_output(self):
#         return self.current_value

#     def check_finished(self):
#         return self.is_finished

#     def kill(self):
#         print("deleted: " + str(self))
#         del self