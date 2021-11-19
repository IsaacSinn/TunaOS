import pygame
import threading
from threading import Thread
from pubsub import pub
import time
import can
import at_serial_can

class pygameLoop(threading.Thread):
    def __init__(self):
        super(pygameLoop, self).__init__()

    def run(self):
        pygame.init()
        while True:
            pygame.event.pump()
            time.sleep(0.1)


class gui(threading.Thread):
    def __init__(self):
        super(gui, self).__init__()
        pygame.display.set_caption("GUI")
        self.screen = pygame.display.set_mode((800, 600))

        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('#00FF00'))

        self.is_running = True

        pygame.font.init()
        self.font = pygame.font.SysFont("Comic Sans MS", 30)

    def run(self):
        while self.is_running:
            print("running")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            text = self.font.render(f"", False, (0,0,0))

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(text, (0,0))

            pygame.display.update()




class joystick(threading.Thread):

    def __init__(self):
        #pygame.init()
        pygame.joystick.init()
        self.direct_input = [0 for i in range(6)]
        self.output_power = 0

        try:
            self.joystick = pygame.joystick.Joystick(0)
        except:
            raise TypeError("No joystick connected")
        self.joystick.init()
        super(joystick, self).__init__()

    def run(self):
        while True:
            time.sleep(0.1)
            for i in range(self.joystick.get_numaxes()):
                self.direct_input[i] = self.joystick.get_axis(i)
                LUD = self.direct_input[1]

            if LUD >= 0:
                self.output_power = int(LUD*32767)
            else:
                self.output_power = int(LUD*32768)

            print("output_power: " , self.output_power)
            pub.sendMessage("can.send", message = {"address": 0xFF, "data": [32, self.output_power >> 8 & 0xFF, self.output_power & 0xFF]})

class CAN_Handler(threading.Thread):

    def __init__(self):
        pub.subscribe(self.message_listener, "can.send")
        self.bus = at_serial_can.ATSerialBus(channel = "COM3", bitrate=250000)
        super(CAN_Handler, self).__init__()

    def message_listener(self, message):
        msg  = can.Message(arbitration_id = message["address"], data = message["data"], is_extended_id = False)
        print("msg sent:", msg)
        self.bus.send(msg)

    def run(self):
        while True:
            time.sleep(0.1)
            print("msg received")
            msg = self.bus.recv(0)
            #print("can bus received: ", msg)

if __name__ == '__main__':
    pygameloop = pygameLoop()
    pygameloop.start()

    time.sleep(1)

    CAN_Handler = CAN_Handler()
    joystick = joystick()

    CAN_Handler.start()
    joystick.start()

    gui = gui()
    gui.start()
