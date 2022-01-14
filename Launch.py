import time
from ModuleBase import ModuleManager
from PyGameServices import PyGameServices

# Modules
from GUI import GUI
from Joystick import Joystick
from ControlProfile import ControlProfile
from ThrusterPower import ThrusterPower
from Thrusters import Thrusters

mm = ModuleManager()
pygs = PyGameServices()
pygs.start(60)

GUI = GUI()
Joystick = Joystick()
ControlProfileA = ControlProfile(100, 30, "A")
ControlProfileB = ControlProfile(70, 50, "B")
ControlProfileC = ControlProfile(50, 50, "C")
ControlProfileD = ControlProfile(30, 50, "D")
ThrusterPower = ThrusterPower()
Thrusters = Thrusters()

mm.register((Joystick, 120), (ControlProfileA, 60), (ControlProfileB, 60), (ControlProfileC, 60), (ControlProfileD, 60), (ThrusterPower, 60), (Thrusters, 60))
#mm.register((Joystick, 120), (GUI, 60))

mm.start_all()
