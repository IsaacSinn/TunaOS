import time
from ModuleBase import ModuleManager
from PyGameLoop import PyGameLoop

# mm = ModuleManager()
# mm.register(("Joystick", "Joystick", 60), ("GUI", "GUI", 60))
# PyGameLoop = PyGameLoop()
# PyGameLoop.start(60)
# mm.start_all()




from Joystick import Joystick
from GUI import GUI
from PyGameLoop import PyGameLoop

GUI = GUI()
GUI.start(60)

PyGameLoop = PyGameLoop()
PyGameLoop.start(60)

Joystick = Joystick()
Joystick.start(60)


# Conditions that work:
# --> Module instantiated and started at the same time AND Joystick instantiated, started after PyGameLoop
