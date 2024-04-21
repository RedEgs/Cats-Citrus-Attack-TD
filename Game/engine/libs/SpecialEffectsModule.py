import pytweening, pygame, sys, os, time, math
    
def dropshadow(image: pygame.Surface, radius):
    shadow_base = image
    base_width = shadow_base.get_size()[0]  
    base_height = shadow_base.get_size()[1]

    # Create a black surface with the same size as the image
    black_surf = shadow_base.copy()
    black_surf.fill((0,0,0))  # Adjust alpha value as needed for darkness

    # Buffer surface for the shadow, increase size to accommodate the entire shadow
    buffer_width = base_width + 10 * radius
    buffer_height = base_height + 10 * radius
    buffer_surf = pygame.Surface((buffer_width, buffer_height), pygame.SRCALPHA)
    pos =  black_surf.get_rect(center = buffer_surf.get_rect().center)
    
    
    buffer_surf.blit(black_surf, pos)
    buffer_surf = pygame.transform.gaussian_blur(buffer_surf, 10)
    
    buffer_surf.blit(shadow_base, pos)
    buffer_surf.get_rect(topleft=(image.get_rect().topleft))
   
    
    return buffer_surf
     
          
def aa_outline(image: pygame.Surface, outline_color, thickness):
    # Has to double the size. Because you - left and add to width to push right.
    outline_surf = pygame.transform.smoothscale(image, (image.get_size()[0]+thickness, 
                                                        image.get_size()[1]+thickness))
    outline_surf.fill((outline_color), None, pygame.BLEND_RGB_MAX)

    
    outline_surf.blit(image, (0+thickness//2, 0+thickness//2))
    return outline_surf

