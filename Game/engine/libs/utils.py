import pygame, json, os, sys

def is_in_list(item, list):
    return item in list
    
def sleep(seconds):
    """
    Sleep for a specified number of seconds.

    Parameters:
    - seconds: The time to sleep in seconds.
    """
    milliseconds = seconds * 1000  # Convert seconds to milliseconds
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < milliseconds:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def wait(seconds, callback=None):
    """
    Wait for a specified number of seconds and execute a callback when the time is up.

    Parameters:
    - seconds: The time to wait in seconds.
    - callback: The function to execute when the time is up.
    """
    milliseconds = seconds * 1000  # Convert seconds to milliseconds
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < milliseconds:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # Execute the callback if provided
    if callback is not None:
        callback()

