
'''
CAN_Handler Module

Subscribe Topics:

can.send
    "address": <hexadecimal>
    "data" <bytearrray>

Publish Topics:

log.sent:
    message frame

can.receive.<arbitration_id>:
    "data" <bytearray>
    "extra" <dictionary>
	"timestamp" <float>

'''
import can
import at_serial_can
from ModuleBase import Module
from pubsub import pub
import threading

class CANHandler(Module):
    def __init__(self):
        super().__init__()
        
        connected = False
        self.counter = 0

        for i in range(20):
            try:
                self.bus = at_serial_can.ATSerialBus(channel=f"COM{i}", ttyBaudrate=115200, bitrate=250000)
                print(f"Connected COM{i}")
                connected = True
                break
            except:
                pass
        
        if not connected:
            raise Exception("NOT Connected to any CAN BUs sender, goodbye, check cable")

        pub.subscribe(self.message_listener, "can.send")
        
        self.lock = threading.Lock()

    def message_listener(self, message):
        msg = can.Message(arbitration_id = message["address"], data = message["data"], is_extended_id = False)
        ######
        self.lock.acquire()
        ######
        try:
            self.bus.send(msg, timeout=0.01)
            pub.sendMessage(f"log.sent.{msg.arbitration_id}" , message = msg)
        #TODO: Handle different types of errors
        except Exception as e:
            print("Message not sent:", [e, msg])
        finally:  
            ######
            self.lock.release()
            ######

    def run(self):
        msg = self.bus.recv(0)

        if msg is not None:
            topic = f"can.receive.{hex(msg.arbitration_id)}"
            pub.sendMessage(topic, message = {"can.receive": msg})



if __name__ == "__main__":
    pass
