import pytweening, pygame, sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
resources_dir = os.path.join(current_dir, '..', '..', 'resources')

from ..libs.utils import *
from ..libs.scenes import *
from ..libs.transitions import *
from ..libs.tween import *

class Director(self):
    def __init__(self, screen):
        self.screen = screen
       
    def events(self):
        pass   
        
    def draw(self):    
        pass
        
    def update(self):
        pass
        
    def run(self):
        self.events()
        self.draw()
        self.update()
        
    
    