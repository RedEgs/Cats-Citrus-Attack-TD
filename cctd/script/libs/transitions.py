import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.utils import *
from ..libs.scenes import *

class TransitionDirector:
    def __init__(self, screen):
        self.transitions = []

        self.isTransitioning = len(self.transitions) == 1
        self.canTransition = not self.isTransitioning 

    def add_transition(self, transition):
        if len(self.transitions) < 1:
            self.transitions.append(transition)

    def remove_transition(self):
        self.transitions.clear()

    def update(self):
        for transition in self.transitions:
            transition.update()
            transition.draw()

class Transition:
    def __init__(self, screen, scene_director, transition_director, from_scene, to_scene):
        self.transition_director = transition_director
        self.sceneDirector = scene_director
        self.screen = screen
        self.from_scene = from_scene
        self.to_scene = to_scene

        self.curr_percentage = 0
        self.half = False
        self.completed = False

        self.add_transition()
    
    def kill_transition(self):
        self.transition_director.remove_transition()
    
    def add_transition(self):
        self.transition_director.add_transition(self)

    def update(self):
        pass

    def draw(self):
        pass
        #self.screen.fill((255,0,0))

    def run(self):
        self.update()
        self.draw()

class FadeTransition(Transition):
    def __init__(self, screen, scene_director,  transition_director, from_scene, to_scene , timing):
        super().__init__(screen, scene_director, transition_director, from_scene, to_scene)
        
        self.timing = timing

        loadingImage = pygame.image.load(
            os.path.join(resources_dir, "loading", "loading_screen.png")).convert_alpha()
        
        
        self.FadeIn = TweenOpacity(
            0, 255, loadingImage, timing, pytweening.easeInOutQuad)
        self.FadeOut = TweenOpacity(
            255, 0, loadingImage, timing, pytweening.easeInOutQuad)

        self.FadeIn.start()

    def kill_transition(self):
        return super().kill_transition()

    def add_transition(self):
        return super().add_transition()

    def update(self):
        self.FadeIn.update()
        self.FadeOut.update()

        if self.curr_percentage == self.timing * 100:
            self.sceneDirector.set_scene(self.to_scene) # Change the scene while black
            self.FadeOut.start()
                
        if self.curr_percentage == self.timing * 200:
            self.kill_transition()
            self.completed = True
    
        self.curr_percentage += 1


    def draw(self):
        self.FadeIn.draw(self.screen)
        self.FadeOut.draw(self.screen)
    





