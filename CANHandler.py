
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
from infi.devicemanager import DeviceManager

class CANHandler(Module):
    def __init__(self, baudrate):
        super().__init__()
        
        connected = False
        self.baudrate = baudrate
        self.lock = threading.Lock()
        self.port = None
        
        dm = DeviceManager()
        dm.root.rescan()
        for d in dm.all_devices:
            if "USB-SERIAL CH340" in d.description:
                self.port = "COM" + d.description[-2]
                self.bus = at_serial_can.ATSerialBus(channel= self.port, ttyBaudrate=self.baudrate, bitrate=250000)
                print(f"Connected {self.port}")
                connected = True
        
        if not connected:
            raise Exception("NOT Connected to any CAN BUs sender, goodbye, check cable")

        pub.subscribe(self.message_listener, "can.send")
    

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
    CANHandler = CANHandler(115200)
