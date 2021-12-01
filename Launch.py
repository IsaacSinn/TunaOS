from Joystick import Joystick
from GUI import GUI
from PyGameLoop import PyGameLoop

GUI = GUI()
GUI.start(60)
PyGameLoop = PyGameLoop()
PyGameLoop.start(60)
Joystick = Joystick()
Joystick.start(60)
