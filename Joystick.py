from ModuleBase import Module
import pygame
from pubsub import pub

# constants
DEADZONE_THRESHOLD_L = 0.1
DEADZONE_THRESHOLD_R = 0.1
DEADZONE_THRESHOLD_Z = 0.1

def deadzoneleft(X):
    if X <(DEADZONE_THRESHOLD_L) and X > (-DEADZONE_THRESHOLD_L):
        return 0
    else:
        return X
def deadzoneright(X):
    if X <(DEADZONE_THRESHOLD_R) and X > (-DEADZONE_THRESHOLD_R):
        return 0
    else:
        return X

def deadzone_back(value):
    if value <(DEADZONE_THRESHOLD_Z) and value > (-DEADZONE_THRESHOLD_Z):
        return 0
    else:
        return value

class Joystick(Module):

    def __init__(self):
        super().__init__()

        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(0)
        except:
            raise TypeError("No joystick connected")
        self.joystick.init()

        # variables
        self.direct_input = [0 for i in range(6)]
        self.movement_message = [0 for i in range(6)]
        self.control_invert = False

    def run(self):

        for i in range(self.joystick.get_numaxes()):
            self.direct_input[i] = self.joystick.get_axis(i)

        LLR, LUD, RLR, RUD, BL, BR = self.direct_input
        print(self.direct_input)
        LLR = 1*deadzoneleft(LLR)
        LUD = -1*deadzoneleft(LUD)
        RLR = 1*deadzoneright(RLR)
        RUD = -1*deadzoneright(RUD)

        BL = -((BL + 1) / 2)
        BR = (BR + 1) / 2
        BLR = deadzone_back(BL + BR)

        if self.control_invert:
            self.movement_message = [-LLR, -LUD, -RLR, BLR, -RUD, 0]
        else:
            self.movement_message = [ LLR,  LUD, -RLR, BLR,  RUD, 0]    #(strafe, drive, yaw, updown, tilt, 0)

        pub.sendMessage("joystick.movement", message = {"joystick_movement": self.movement_message})



if __name__ == '__main__':

    Joystick = Joystick()
    Joystick.start(60)
