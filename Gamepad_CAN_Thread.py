import pygame
import threading
from threading import Thread
from pubsub import pub
import time
import time
import can
import at_serial_can


class joystick(threading.Thread):

    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.direct_input = [0 for i in range(6)]
        self.output_power = 0

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
                LUD = self.direct_input[1]

            if LUD >= 0:
                self.output_power = int(LUD*32767)
            else:
                self.output_power = int(LUD*32768)

            print("output_power: " , self.output_power)
            pub.sendMessage("can.send", message = {"address": 0xFF, "data": [32, self.output_power >> 8 & 0xFF, self.output_power & 0xFF]})

class CAN_Handler(threading.Thread):

    def __init__(self):
        print("CAN_HANDLER INIT")
        pub.subscribe(self.message_listener, "can.send")
        self.bus = at_serial_can.ATSerialBus(channel = "COM3", bitrate=250000)
        threading.Thread.__init__(self.receive(), dameon=True)

    def message_listener(self, message):
        msg  = can.Message(arbitration_id = message["address"], data = message["data"], is_extedned_id = False)
        print("msg sent:", msg)
        #self.bus.send(msg)

    def receive(self):
        time.sleep(0.1)
        print("msg received")
        #msg = self.bus.recv(0)
        #print("can bus received: ", msg)



if __name__ == '__main__':
    CAN_Handler = CAN_Handler()
    CAN_Handler.start()
    joystick = joystick()
    joystick.start()
