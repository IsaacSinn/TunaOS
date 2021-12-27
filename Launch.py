import time
from ModuleBase import ModuleManager, Module
from threading import Thread
import pygame

class main_loop(Module):
    def run(self):
        pygame.init()
        if pygame.display.get_init():
            pygame.display.flip()
            pygame.event.pump()


main_loop = main_loop().start(60)

mm = ModuleManager()
mm.register(("GUI", "GUI", 60), ("Joystick", "Joystick", 60))
mm.start_all()






# from Joystick import Joystick
# from GUI import GUI
# from PyGameLoop import PyGameLoop
#
# PyGameLoop = PyGameLoop()
# PyGameLoop.start(60)
#
# GUI = GUI()
# Joystick = Joystick()
#
# GUI.start(60)
# Joystick.start(60)


# Conditions that work:
# --> Module instantiated and started at the same time AND Joystick instantiated, started after PyGameLoop
