import pygame
from ModuleBase import Module

class PyGameServices(Module):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PyGameServices, cls).__new__(cls)
            cls.pygame_init = False
            cls.screen = None
            cls.joystick = None
        return cls.instance

    @classmethod
    def run(cls):

        if not cls.pygame_init: # run once

            pygame.init()
            pygame.display.init()
            pygame.font.init()
            cls.pygame_init = True

        if cls.screen: # run if screen initialized
            pygame.display.flip()

        pygame.event.pump()

    @classmethod
    def get_pygame(cls):
        return pygame

    @classmethod
    def get_screen(cls, caption, mode = (1920, 1080)):
        pygame.display.set_caption(caption)
        cls.screen = pygame.display.set_mode(mode)
        return cls.screen

    @classmethod
    def get_joystick(cls, ID = 0):
        try:
            cls.joystick = pygame.joystick.Joystick(ID)
            cls.joystick.init()
            return cls.joystick
        except:
            return None
