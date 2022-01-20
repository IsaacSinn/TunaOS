from ModuleBase import Module
from pubsub import pub

EMLRcommand = {
                "EM_L": {1 : [0x30, 0x10], 0: [0x30, 0x00]},
                "EM_R": {1 : [0x31, 0x10], 0: [0x31, 0x00]},
                }

class EM(Module):
    def __init__(self, device, address):
        super().__init__()
        self.device = device
        self.address = address
        exec(f"pub.subscribe(self.Listener, 'gamepad.{self.device}')")

    def run(self):
        pass

    def Listener(self, message):
        #print(self.device, message)
        pub.sendMessage("can.send", message = {"address": eval(self.address), "data": EMLRcommand["EM_L"][1 if message["L"] else 0]})
        pub.sendMessage("can.send", message = {"address": eval(self.address), "data": EMLRcommand["EM_R"][1 if message["R"] else 0]})

class __Test_Case_Send__(Module):
    def __init__(self):
        super().__init__()
        pub.subscribe(self.Listener, "can.send")

    def run(self):
        pub.sendMessage("gamepad.EM1", message = {"L": True, "R": False})

    def Listener(self, message):
        print(message)

if __name__ == "__main__":
    pass
