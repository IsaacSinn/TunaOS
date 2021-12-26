from ModuleBase import Module
import pygame
from pubsub import pub

class PyGameLoop(Module):
    def __init__(self):
        super().__init__()
        self.pygame_init = False

    def run(self):
        if not self.pygame_init:
            pygame.init()
            self.pygame_init = True

        pygame.event.pump()

        try:
            pygame.display.flip()
        except ImportError:
            print("GUI Module not imported")
