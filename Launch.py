import time
from ModuleBase import ModuleManager

# mm = ModuleManager()
# mm.register(("Joystick", "Joystick", 60), ("PyGameLoop", "PyGameLoop", 60), ("GUI", "GUI", 60))
# mm.start_all()





from GUI import GUI
GUI = GUI()
from Joystick import Joystick
Joystick = Joystick()

from PyGameLoop import PyGameLoop
PyGameLoop = PyGameLoop()
PyGameLoop.start(60)






GUI.start(60)
Joystick.start(60)
