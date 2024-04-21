from engine.libs.Services import Service
import pygame, pytweening, json, os, sys

import engine.libs.TweenService as TweenService
import engine.libs.GuiService as GuiService
import engine.libs.Utils as Utils


class TransitionService(Service):
    transitions = []

    isTransitioning = len(transitions) == 1
    canTransition = not isTransitioning

    @classmethod
    def add_transition(cls, transition):
        if len(cls.transitions) < 1:
            cls.transitions.append(transition)

    @classmethod
    def remove_transition(cls, transition):
        cls.transitions.clear()
        del transition

    @classmethod
    def update(cls):
        for transition in cls.transitions:
            transition.update()

    @classmethod
    def draw(cls, screen):
        for transition in cls.transitions:
            transition.draw(screen)


class Transition:
    def __init__(self, from_scene, to_scene):
        self.from_scene = from_scene
        self.to_scene = to_scene

        self.curr_percentage = 0
        self.half = False
        self.completed = False

        TransitionService.add_transition(self)

    def kill_transition(self):
        TransitionService.remove_transition(self)

    def update(self):
        pass

    def draw(self):
        pass


class FadeTransition(Transition):
    def __init__(self, from_scene, to_scene, app, timing):
        super().__init__(from_scene, to_scene)
        self.app = app

        self.timing = timing
        self.loading_image = pygame.Surface((1280, 720))
        self.loading_image.fill((0))


        # fade_data = TweenService.TweenData(0, 255, timing, 0)
        # self.fade = TweenService.Tween(fade_data)
        # self.fade.start(False, True)

    def update(self):
        if self.curr_percentage == self.timing * 100:
            self.app.scene_service.set_scene(self.to_scene)  # Change the scene while black

        if self.curr_percentage == self.timing * 200:
            self.completed = True

        self.curr_percentage += 1

        if self.completed:
            self.kill_transition()

    def percentage_to_opacity(self, percentage):
            # Ensure percentage is within the range [0, 100]
        percentage = max(0, min(100, percentage))
        
        if percentage <= 50:
            # Map the percentage to the range [0, 50]
            mapped_percentage = (percentage / 50) * 100
        else:
            # Map the percentage to the range [50, 100]
            mapped_percentage = ((100 - percentage) / 50) * 100
            
        # Map the mapped_percentage to the opacity range [0, 255]
        return int((mapped_percentage / 100) * 255)


    def draw(self, screen):
        print("drawing trans")
        if self.curr_percentage >= self.timing * 50:
            #print(self.percentage_to_opacity(self.curr_percentage))
            self.loading_image.set_alpha( self.percentage_to_opacity(self.curr_percentage))
            
        elif self.curr_percentage <= self.timing * 100:
            #print(self.percentage_to_opacity(self.curr_percentage))
            self.loading_image.set_alpha( self.percentage_to_opacity(self.curr_percentage) - 25)
       
        screen.blit(self.loading_image, (0,0))
        # Make sure that the image isnt scene specific.

class WipeTransition(Transition):
    def __init__(self, from_scene, to_scene, app, timing):
        super().__init__(from_scene, to_scene)
        self.app = app

        self.timing = timing
        self.loading_image = pygame.Surface((1280, 720))
        self.loading_image.fill((0))

        self.wipe = TweenService.Tween(1300, 0, 1, pytweening.easeInOutSine, reverse=True, reverse_once=True)
        # fade_data = TweenService.TweenData(0, 255, timing, 0)
        # self.fade = TweenService.Tween(fade_data)
        # self.fade.start(False, True)

    def update(self):
        print(self.wipe.get_progress())
        if self.curr_percentage == self.timing * 0:
            self.wipe.start()
             
        if self.wipe.progress >= .99:
            self.app.scene_service.set_scene(self.to_scene)  # Change the scene while black

        if self.completed:
            self.kill_transition()

    def draw(self, screen):
        self.pos = self.wipe.get_output()
        # if self.curr_percentage >= self.timing * 50:
        #     #print(self.percentage_to_opacity(self.curr_percentage))
        #     self.pos = self.r_wipe.get_output()
            
            
        # elif self.curr_percentage <= self.timing * 100:
        #     #print(self.percentage_to_opacity(self.curr_percentage))
            
            
            
       
        # Make sure that the image isnt scene specific.
        screen.blit(self.loading_image, (self.pos,0))