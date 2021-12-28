from ModuleBase import Module
import pygame
from pubsub import pub

class PyGameLoop(Module):
    def __init__(self):
        super().__init__()
        self.pygame_init = False

    def run(self):
        pygame.init()
        pygame.event.pump()
        pygame.display.flip()
