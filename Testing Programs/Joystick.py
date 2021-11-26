from ModuleBase import Module
import pygame
import pubsub

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

    def run(self):

        for i in range(self.joystick.get_numaxes()):
            self.direct_input[i] = self.joystick.get_axis(i)

        print(self.direct_input)
        #pub.sendMessage("can.send", message = {"address": 0xFF, "data": [32, self.output_power >> 8 & 0xFF, self.output_power & 0xFF]})

class PygameLoop(Module):
    def __init__(self):
        super().__init__()
        self.pygame_init = False

    def run(self):
        if not self.pygame_init:
            pygame.init()
            self.pygame_init = True

        pygame.event.pump()
        #pygame.display.flip()


if __name__ == '__main__':
    PygameLoop = PygameLoop()
    PygameLoop.start(60)

    Joystick = Joystick()
    Joystick.start(60)
