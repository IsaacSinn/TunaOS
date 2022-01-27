
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

class CANHandler(Module):
    def __init__(self):
        super().__init__()

        for i in range(10):
            try:
                self.bus = at_serial_can.ATSerialBus(channel=f"COM{i}", bitrate=250000)
                print(f"Connected COM{i}")
            except:
                pass

        pub.subscribe(self.message_listener, "can.send")

    def message_listener(self, message):
        msg = can.Message(arbitration_id = message["address"], data = message["data"], is_extended_id = False)

        try:
            self.bus.send(msg)
            pub.sendMessage("log.sent" , message = msg)

        except can.CanError:
            print("Message not sent")

    def run(self):
        msg = self.bus.recv(0)

        if msg is not None:
            topic = f"can.receive.{hex(msg.arbitration_id)}"
            pub.sendMessage(topic, message = {"can.receive": msg})



if __name__ == "__main__":
    pass
