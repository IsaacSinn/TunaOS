# TODO: Change serial bandwidth for CAN-USB, 


import time
from ModuleBase import ModuleManager
from PyGameServices import PyGameServices

# MODULES
from GUI import GUI
from Joystick import Joystick
from ControlProfile import ControlProfile
from ThrusterPower import ThrusterPower
from Thrusters import Thrusters
from CANHandler import CANHandler
from EM import EM
from Gripper import Gripper
from Logger import Logger
from Actuator import Actuator

mm = ModuleManager()
pygs = PyGameServices()
pygs.start(100)

GUI_FPS = 60

GUI = GUI()
Joystick = Joystick()
ControlProfileA = ControlProfile(100, 30, "A")
ControlProfileB = ControlProfile(70, 50, "B")
ControlProfileC = ControlProfile(50, 50, "C")
ControlProfileD = ControlProfile(30, 50, "D")
ThrusterPower = ThrusterPower()
Thrusters = Thrusters()
CANHandler = CANHandler()
Logger = Logger(False, True, None, "log.sent.0x23") # FILE, PRINT, RATE_LIMITER, TOPICS

# TOOLS
EM1 = EM("EM1", "0x32")
EM2 = EM("EM2", "0x30")
Gripper = Gripper("gripper", "0x23", "11000") # SPEED 0 - 32767
Actuator = Actuator("actuator", "0x22", "11000")

# REGISTERING MODULES (INSTANCE, REFRESH PER SECOND)
mm.register(
            (GUI, GUI_FPS),
            (Joystick, 60),
            (ControlProfileA, 1),
            (ControlProfileB, 1),
            (ControlProfileC, 1),
            (ControlProfileD, 1),
            (ThrusterPower, 60),
            (Thrusters, 15),
            (CANHandler, 1),
            (EM1, 5),
            (EM2, 5),
            (Gripper, 10),
#            (Actuator, 5)
)

mm.start_all()

while True:
    pygs.get_pygame().event.get()
    pygs.get_pygame().time.delay((2)) # ms