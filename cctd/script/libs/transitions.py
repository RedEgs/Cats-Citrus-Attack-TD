import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.utils import *
from ..libs.tween import *
from ..libs.scenes import *

class TransitionDirector:
    def __init__(self, screen):
        self.tween_director = TweenDirector()
        self.transitions = []

        self.isTransitioning = len(self.transitions) == 1
        self.canTransition = not self.isTransitioning 

    def add_transition(self, transition):
        if len(self.transitions) < 1:
            self.transitions.append(transition)

    def remove_transition(self):
        self.transitions.clear()

    def update(self):
        self.tween_director.update()
        
        for transition in self.transitions:
            transition.update()
            transition.draw()

class Transition:
    def __init__(self, screen, scene_director, transition_director, from_scene, to_scene):
        self.transition_director = transition_director
        self.scene_director = scene_director
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

        self.loading_image = load_image(os.path.join(resources_dir, "loading", "loading_screen.png")).convert_alpha()
        
        
        self.Fade = Tween(opacity_fade_data, self.transition_director.tween_director)

        self.Fade.start(False, True)

    def kill_transition(self):
        return super().kill_transition()

    def add_transition(self):
        return super().add_transition()

    def update(self):
        if self.curr_percentage == self.timing * 100:
            self.Fade.reverse(False)
            self.scene_director.set_scene(self.to_scene) # Change the scene while black
            
                
        if self.curr_percentage == self.timing * 200:
            self.kill_transition()
            self.Fade.kill()
            self.completed = True
    
        self.curr_percentage += 1


    def draw(self):
        self.loading_image.set_alpha(self.Fade.get_output())
        self.screen.blit(self.loading_image, (0,0))





