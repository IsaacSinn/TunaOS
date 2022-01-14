
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

class CAN_Handler(Module):
    def __init__(self):
        super().__init__()
        self.bus = at_serial_can.ATSerialBus(channel="COM4", bitrate=250000)
        pub.subscribe(self.message_listener, "can.send")

    def message_listener(self, message):
        msg = can.Message(arbitration_id = message["address"], data = message["data"], is_extended_id = False)
        self.bus.send(msg)
        pub.sendMessage("log.sent" , message = msg)

    def run(self):
        msg = self.bus.recv(0)
        topic = f"can.receive.{arbitration_id}"

        if msg is not None:
            pub.sendMessage(topic, msg)



if __name__ == "__main__":
    pass
