from ModuleBase import Module
from PyGameServices import PyGameServices
from pubsub import pub

class GUI(Module):
    def __init__(self):
        super().__init__()

        # variables
        self.movement = [0 for i in range(6)]
        self.mode = (800, 800)

        # request from PyGameServices
        pygs = PyGameServices()
        self.screen = pygs.get_screen("Control Program GUI", self.mode)
        self.pygame = pygs.get_pygame()

        # Variables and initialization
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.yellow = (255, 200, 0)
        self.asian_skin = (255,224,196)
        self.dark_skin = (226, 185, 143)
        self.dark_red = (113,2,0)
        self.turquoise = '#9cc3cd'


        self.background = self.pygame.Surface(self.mode)
        self.background.fill(self.pygame.Color(self.turquoise))
        self.font = self.pygame.font.SysFont("Comic Sans MS", 30)
        self.active_tools = ("gamepad.gripper", "gamepad.EM1", "gamepad.EM2", "gamepad.erector")



        def plottings(point_x,point_y,offset_x, offset_y):
            coord_x = point_x * 80 + offset_x
            coord_y = point_y * -80 + offset_y
            pygame.draw.circle(self.screen,yellow,(coord_x, coord_y), 15)

        # pubsub init
        pub.subscribe(self.direct_handler, "gamepad.direct")



    # pubsub handler
    def direct_handler(self, message):
        self.movement = message["gamepad_direct"]

    def run(self):
        text = self.font.render(f"{self.movement}", False, (0,0,0))

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(text, (0,0))

        LLR, LUD, RLR, RUD,BL,BR = (self.movement)

        def dcircle(colour, coords, size):
            self.pygame.draw.circle(self.screen, (colour), (coords), size)


        def dots_back():
            for i in range(4):
                dcircle((i*50,i*50,i*50),(500,200),120-i*30)
                dcircle((i*50,i*50,i*50),(200,200),120-i*30)

        def rect(colour, dimensions,):
            self.pygame.draw.rect(self.screen,colour, self.pygame.Rect(dimensions))

        def plottings(point_x, point_y, offset_x, offset_y):
            coord_x = point_x * 80 + offset_x
            coord_y = point_y * -80 + offset_y
            dcircle((0,200,0),(coord_x,coord_y),20)

        def em_back():
            rect(self.yellow,50,100,200,50)

        dots_back()
        plottings(LLR,-LUD,200,200)
        plottings(RLR,-RUD,500,200)




