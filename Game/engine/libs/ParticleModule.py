import pygame, time, sys, os, math

class Particle:
    image_cache = {}
    
    def __init__(self, 
        pos,
        velocity,
        size,
        color,
        fade_speed = 0
    ):

        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(velocity)
        self.size = size
        self.color = color
        self.fade_speed = fade_speed
        self.alpha = 255
        
        self.active = 1
        
        self.update_image()
     
     
    def check_alpha(self):
        if self.alpha <= 0:
            self.active = 0

     
    def update(self, delta_time):
        self.pos += self.vel * delta_time
        
        if self.fade_speed:
            self.alpha -= self.fade_speed * delta_time
            self.image.set_alpha(self.alpha)
            self.check_alpha()
        
        return self.active
        
        
    def update_image(self):
        cache_lookup = (self.size, self.color, self.alpha)
        
        if not (image_cache := self.image_cache.get(cache_lookup, None)):
            image_cache = pygame.Surface((self.size, self.size))
            image_cache.fill(self.color)
            image_cache.set_alpha(self.alpha)
            
        self.image = image_cache
        
    
class ParticleEmitter: # 21,400 at 60fps 
    def __init__(self, app, particle_limit = False):
        """
        Particle limit - makes sure particles cant be created if fps drops below 60 ( May create wierd behaviour)
        """
        self.app = app
        
        self.particles = []
        self.particle_limit = particle_limit

    

    def update(self, delta_time):
        self.particles = [particle for particle in self.particles if particle.update(delta_time)]
        
    def add(self, particles):
        if self.particle_limit and self.app.get_fps() < 60:
            pass
        else:
            self.particles.extend(particles)
        
    def draw(self, surface):
        surface.fblits([(particle.image, particle.pos) for particle in self.particles])
    
    
    
    
    
    def __len__(self):
        return len(self.particles)