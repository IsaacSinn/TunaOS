import time
from ModuleBase import ModuleManager
from PyGameServices import PyGameServices

# Modules
from GUI import GUI
from Joystick import Joystick
from ControlProfile import ControlProfile
from ThrusterPower import ThrusterPower
from Thrusters import Thrusters
from CANHandler import CANHandler
from EM import EM
from Gripper import Gripper
from Logger import Logger

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
#CANHandler = CANHandler()
Logger = Logger(False, True, "log")

# TOOLS
EM1 = EM("EM1", "0x30")
EM2 = EM("EM2", "0x32")
Gripper = Gripper("gripper", "0x22", "10000") # speed 0 - 32767

# Registering Modules
mm.register(
            (Joystick, 120),
            (ControlProfileA, 60),
            (ControlProfileB, 60),
            (ControlProfileC, 60),
            (ControlProfileD, 60),
            (ThrusterPower, 60),
            (Thrusters, 60),
#            (CANHandler, 60),
            (EM1, 1),
            (EM2, 1),
            (Gripper, 1)
)

# FOR TESTING GUI (HOU FONG)
# mm.register((Joystick, 120), (GUI, 60))

mm.start_all()
