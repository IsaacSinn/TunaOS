from ModuleBase import Module
from pubsub import pub
import time

class TransectLine(Module):
    def __init__(self, speed, flip, time):
        super().__init__()
        self.flip = flip
        self.speed = speed
        self.activate = False
        self.time = time
        
        if self.flip:
            self.speed = -self.speed
        
        pub.subscribe(self.Listener, "gamepad.transect")

    def run(self):
        while (time.time() - self.initial) < self.time and self.activate:
            pub.sendMessage("gamepad.movement", message = {"gamepad_movement":[0, self.speed, 0, 0, 0, 0]})
        self.activate = False

    def Listener(self, message):   
        self.state = message["gamepad_transect"]
        
        if self.state:
            self.initial = time.time()
            self.activate = True
        else:
            self.activate = False

if __name__ == "__main__":
    pass
