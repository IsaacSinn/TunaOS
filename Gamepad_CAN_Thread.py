import pygame
import threading
from threading import Thread
from pubsub import pub
import time
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
            time.sleep(0.01)

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
            #pygame.event.pump()
            for i in range(self.joystick.get_numaxes()):
                self.direct_input[i] = self.joystick.get_axis(i)
                LUD = self.direct_input[1]
            print(self.direct_input)
            '''
            if LUD >= 0:
                self.output_power = int(LUD*32767)
            else:
                self.output_power = int(LUD*32768)

            print("output_power: " , self.output_power)
            pub.sendMessage("can.send", message = {"address": 0xFF, "data": [32, self.output_power >> 8 & 0xFF, self.output_power & 0xFF]})
            '''
class CAN_Handler(threading.Thread):

    def __init__(self):
        pub.subscribe(self.message_listener, "can.send")
        self.bus = at_serial_can.ATSerialBus(channel = "COM3", bitrate=250000)
        super(CAN_Handler, self).__init__()

    def message_listener(self, message):
        msg  = can.Message(arbitration_id = message["address"], data = message["data"], is_extended_id = False)
        print("msg sent:", msg)
        #self.bus.send(msg)

    def run(self):
        while True:
            time.sleep(0.1)
            print("msg received")
            #msg = self.bus.recv(0)
            #print("can bus received: ", msg)

# class MyThread(threading.Thread):
#     def __init__(self, name):
#         super(MyThread,self).__init__()
#         self.name = name
#     def run(self):
#         while True:
#             print(self.name)
#             time.sleep(0.6)

if __name__ == '__main__':
    pl = pygameLoop()

    pl.start()

    time.sleep(1)


    #CAN_Handler = CAN_Handler()
    joystick = joystick()

    #CAN_Handler.start()
    joystick.start()

    # a = MyThread("A")
    # b = MyThread("B")
    #
    # a.start()
    # b.start()
