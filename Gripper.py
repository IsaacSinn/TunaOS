from ModuleBase import Module
from pubsub import pub

class Gripper(Module):
    def __init__(self, device, address, speed):
        super().__init__()
        self.device = device
        self.speed = int(speed)
        self.address = address
        exec(f'pub.subscribe(self.Listener, "gamepad.{self.device}")')

    def run(self):
        pass

    def Listener(self, message):
        if message["tool_state"] == 1:
            pub.sendMessage('can.send', message = {"address": eval(self.address), "data": [32, self.speed >> 8 & 0xff, self.speed & 0xff]})
        elif message["tool_state"] == -1:
            pub.sendMessage('can.send', message = {"address": eval(self.address), "data": [32, -self.speed >> 8 & 0xff, -self.speed & 0xff]})
        else:
            pub.sendMessage('can.send', message = {"address": eval(self.address), "data": [32, 0x00, 0x00]})

class __Test_Case_Send__(Module):
    def __init__(self):
        super().__init__()
        pub.subscribe(self.Listener, "can.send")

    def run(self):
        pub.sendMessage("gamepad.gripper", message = {"extend": False, "retract": True})

    def Listener(self, message):
        print(message)

if __name__ == "__main__":
    pass
