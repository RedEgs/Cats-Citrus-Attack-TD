def serialize_surface(surface):
    """Serialize a Pygame surface."""
    import pygame
    
    
    return pygame.image.tostring(surface, 'RGBA'), surface.get_size()

def deserialize_surface(surface_tuple):
    import pygame
    
    """Deserialize a Pygame surface."""
    string, size = surface_tuple
    surface = pygame.Surface(size, pygame.SRCALPHA)
    return pygame.image.fromstring(string, size, 'RGBA')
