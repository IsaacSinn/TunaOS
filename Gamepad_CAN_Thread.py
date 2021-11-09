import pygame
import threading
from threading import Thread
from pubsub import pub
import time
import can
import at_serial_can


class joystick(threading.Thread):

    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        try:
            self.joystick = pygame.joystick.Joystick(0)
        except:
            raise TypeError("No joystick connected")
        self.joystick.init()

        threading.Thread.__init__(self.get_joystick(), daemon=True)

    def get_joystick(self):
        while True:
            pygame.event.pump()
            for i in range(self.joystick.get_numaxes()):
                self.direct_input[i] = self.joystick.get_axis(i)

            pub.sendMessage("joystick.movement", message = {"joystick.movement": self.direct_input})

class CAN_Handler(threading.Thread):

    def __init__(self):
        pub.subscribe(self.message_listener, "joystick.movement")
        self.bus = at_serial_can.ATSerialBus(channel = "COM7", bitrate=250000)
        threading.Thread.__init__(self.receive(), dameon=True)

    def receive(self):
        msg = self.bus.recv(0)
        print(msg)



if __name__ == '__main__':
    joystick = joystick()
    joystick.start()

    CAN_Handler = CAN_Handler()
    CAN_Handler.start()
