import time
from ModuleBase import ModuleManager

mm = ModuleManager()
mm.register(("Joystick", "Joystick", 60), ("PyGameLoop", "PyGameLoop", 60), ("GUI", "GUI", 60))
mm.start_all()

time.sleep(5)
mm.stop("GUI")
