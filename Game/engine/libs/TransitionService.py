import pygame, json, os, sys

import engine.libs.TweenService as TweenService
import engine.libs.GuiService as GuiService
import engine.libs.Utils as Utils


class TransitionService:
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
        self.loading_image = GuiService.ImageElement(
            pygame.display.get_window_size(),
            "cctd/resources/loading/loading_screen.png",
        )

        fade_data = TweenService.TweenData(0, 255, timing, 0)
        self.fade = TweenService.Tween(fade_data)
        self.fade.start(False, True)

    def update(self):
        if self.curr_percentage == self.timing * 100:
            self.fade.reverse(False)
            self.app.scenes.set_scene(self.to_scene)  # Change the scene while black

        if self.curr_percentage == self.timing * 200:
            self.completed = True

        self.curr_percentage += 1

        if self.completed:
            self.kill_transition()

    def draw(self, screen):
        # print("drawing")
        self.loading_image.update_opacity(self.fade.get_output())
        self.loading_image.draw(screen)
        # Make sure that the image isnt scene specific.
