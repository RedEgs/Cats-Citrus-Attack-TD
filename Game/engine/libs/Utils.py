import pygame, json, os, sys

def is_in_list(item, list):
    print(item)
    return item in list
    
def get_item_index(item, list):
    try:
        return list.index(item)
    except ValueError:
        return False
    
def get_center(x, y):
    return x // 2, y //2   

def scale_image_by_res(original_image, target_width, target_height, aspect_ratio):
    # Calculate the width and height based on the aspect ratio
    if (target_width / aspect_ratio) > target_height:
        scaled_width = int(target_height * aspect_ratio)
        scaled_height = target_height
    else:
        scaled_width = target_width
        scaled_height = int(target_width / aspect_ratio)

    # Scale the image
    scaled_image = pygame.transform.scale(original_image, (scaled_width, scaled_height))

    return scaled_image

def scale_image(image, scale_factor):
    """
    Scale the input Pygame image surface by the given factor.

    Parameters:
    - image: The input Pygame image surface.
    - scale_factor: The factor by which to scale the image.

    Returns:
    - The scaled Pygame image surface.
    """

    original_rect = image.get_rect()
    
    new_width = original_rect.width * scale_factor
    new_height = original_rect.height * scale_factor

    scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))

    return scaled_image

def rotate_image(image, angle):
    """
    Rotate the input Pygame image surface by the given angle.

    Parameters:
    - image: The input Pygame image surface.
    - angle: The angle (in degrees) by which to rotate the image.

    Returns:
    - The rotated Pygame image surface.
    """
    rotated_image = pygame.transform.rotate(image, angle)
    return rotated_image

def rotozoom_image(image, angle, scale):
    rotozoomed_image = pygame.transform.rotozoom(image, angle, scale)
    return rotozoomed_image
