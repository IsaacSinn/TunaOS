from ModuleBase import Module
from PyGameServices import PyGameServices
from pubsub import pub

class GUI(Module):
    def __init__(self):
        super().__init__()

        # variables
        self.movement = [0 for i in range(6)]
        self.mode = (1920, 1080)

        # request from PyGameServices
        pygs = PyGameServices()
        self.screen = pygs.get_screen("Control Program GUI", self.mode)
        self.pygame = pygs.get_pygame()

        # Variables and initialization
        self.background = self.pygame.Surface(self.mode)
        self.background.fill(self.pygame.Color('#00FF00'))
        self.font = self.pygame.font.SysFont("Comic Sans MS", 30)
        self.active_tools = ("gamepad.gripper", "gamepad.EM1", "gamepad.EM2", "gamepad.erector")

        # pubsub init
        pub.subscribe(self.direct_handler, "gamepad.direct")

    # pubsub handler
    def direct_handler(self, message):
        self.movement = message["gamepad_direct"]

    def run(self):
        text = self.font.render(f"{self.movement}", False, (0,0,0))

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(text, (0,0))
