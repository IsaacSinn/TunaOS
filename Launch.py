import time
from ModuleBase import ModuleManager

mm = ModuleManager()
mm.register(("PyGameLoop", "PyGameLoop", 60), ("GUI", "GUI", 60), ("Joystick", "Joystick", 60))
mm.start_all()
