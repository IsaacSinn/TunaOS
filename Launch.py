from Joystick import Joystick
from GUI import GUI
from PyGameLoop import PyGameLoop
import time

GUI = GUI()
GUI.start(60)
PyGameLoop = PyGameLoop()
PyGameLoop.start(60)
Joystick = Joystick()
Joystick.start(60)
time.sleep(5)
Joystick.stop()
