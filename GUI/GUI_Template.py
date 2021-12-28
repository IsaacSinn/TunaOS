from GUI_ModuleBase import Module
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

        self.direct_input = [0 for i in range(6)]
        self.movement_message = [0 for i in range(6)]

    def run(self):

        for i in range(self.joystick.get_numaxes()):
            self.direct_input[i] = self.joystick.get_axis(i)

        LLR, LUD, RLR, RUD, BL, BR = self.direct_input
        LLR = 1*LLR
        LUD = -1*LUD
        RLR = 1*RLR
        RUD = -1*RUD

        BL = -((BL + 1) / 2)
        BR = (BR + 1) / 2
        BLR = BL + BR

        self.movement_message = [ LLR,  LUD, -RLR, BLR,  RUD, 0]    #(strafe, drive, yaw, updown, tilt, 0)


        pub.sendMessage("joystick.movement", message = {"joystick_movement": self.movement_message})
        pub.sendMessage("thruster.power", message = {"Thruster_message": [1,1,-1,-1,0,0]}) # [FL, FR, BL, BR, UF, UB]

class PygameLoop(Module):
    def __init__(self):
        super().__init__()
        self.pygame_init = False

    def run(self):
        if not self.pygame_init:
            pygame.init()
            self.pygame_init = True

        pygame.event.pump()
        pygame.display.flip()

class gui(Module):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption("GUI")
        self.screen = pygame.display.set_mode((1000, 400))

        turquoise = '#9cc3cd'

        self.background = pygame.Surface((1000, 400))
        self.background.fill(pygame.Color(turquoise))

        self.is_running = True

        pygame.font.init()
        self.font = pygame.font.SysFont("Comic Sans MS", 30)
        self.movement = [0 for i in range(6)]

        pub.subscribe(self.movement_handler, "joystick.movement")

    def movement_handler(self, message):
        self.movement = message["joystick_movement"]

    def run(self):
        text = self.font.render(f"{self.movement}", False, (0,0,0))

        self.screen.blit(self.background, (0, 0))
        # self.screen.blit(text, (0,0))

        LLR, LUD, RLR, BLR, RUD, X = (self.movement)

        #Base Colors
        white = (255, 255, 255)
        black = (0, 0, 0)
        yellow = (255, 200, 0)
        asian_skin = (255,224,196)
        dark_skin = (226, 185, 143)
        dark_red = (113,2,0)
        turquoise = '#9cc3cd'

        def dots_back():
            pygame.draw.circle(self.screen,black,(500,200),120)
            pygame.draw.circle(self.screen, black,(200,200),120)

        def plottings(point_x,point_y,offset_x, offset_y):
            coord_x = point_x * 80 + offset_x
            coord_y = point_y * -80 + offset_y
            pygame.draw.circle(self.screen,yellow,(coord_x, coord_y), 15)

        dots_back()
        plottings(LLR,LUD,200,200)
        plottings(-RLR,RUD,500,200)

if __name__ == '__main__':
    gui = gui()
    gui.start(60)

    PygameLoop = PygameLoop()
    PygameLoop.start(60)

    Joystick = Joystick()
    Joystick.start(60)
