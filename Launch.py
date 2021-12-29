import time
from ModuleBase import ModuleManager
from PyGameServices import PyGameServices


mm = ModuleManager()
pygs = PyGameServices()
pygs.start(60)

mm.register(("GUI", "GUI", 60), ("Joystick", "Joystick", 60))
mm.start_all()
