import pygame, json, os, sys

def get_dimensions(dimensions):
    """
    Returns dimensions from a resolution, e.g "1920x1080"
    """
    
    width, height = str(dimensions).split("x")
    
    return int(width), int(height)

def get_center(x, y):
    return x // 2, y // 2