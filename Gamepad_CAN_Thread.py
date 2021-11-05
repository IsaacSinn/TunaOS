import pygame
from threading import Thread
from pubsub import pub


class joystick:
    def __init__(self):
        pygame.joystick.JoyStick(0)
        joystick.init()


    def joystick_run():
