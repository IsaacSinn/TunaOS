import time
from ModuleBase import ModuleManager
from PyGameServices import PyGameServices

# Modules
from GUI import GUI
from Joystick import Joystick

mm = ModuleManager()
pygs = PyGameServices()
pygs.start(60)

GUI = GUI()
Joystick = Joystick()

mm.register((GUI, 60), (Joystick, 60))
mm.start_all()
