# Main project file
import pygame, os
from pyredengine import PreviewMain # type: ignore


"""
All code given is the bare minimum to safely run code within the engine.
Removing any code that already exists in not recommended and you WILL run into issues.
When compiled, parts of code are removed to optimise and simplify the file.
"""

class Main(PreviewMain.MainGame):
    def __init__(self, fullscreen = False) -> None:
        super().__init__(fullscreen)
        """
        Make sure not to remove the super() method above, as it will break the whole script.
        """

        self.display = pygame.display.get_surface()


        if self._engine_mode:
            abspath = os.path.abspath(__file__)
            dname = os.path.dirname(abspath)
            os.chdir(dname)

    def handle_events(self):
        """
        All your logic for handling events should go here.
        Its recommended you write code to do with event handling here.
        Make sure that you don't remove the `pygame.QUIT` event as the game won't be able to be shutdown.
        See pygame docs for more info: https://www.pygame.org/docs/ref/event.html.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def update(self):
        """
        This is where you independant code goes.
        This is purely a conceptual seperator from the rest of the game code.
        Think of this as the "body" of your program.
        """
        pass

    def draw(self):
        """
        This is where your drawing code should do.
        Make sure that `pygame.display.flip()` is the last line.
        Make sure that `self.display.fill()` is at the start too.

        """
        self.display.fill((180, 100, 20))
        pygame.display.flip()
