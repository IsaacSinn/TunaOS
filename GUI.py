from ModuleBase import Module
from PyGameServices import PyGameServices
from pubsub import pub

class GUI(Module):
    def __init__(self):
        super().__init__()

        # variables
        self.movement = [0 for i in range(6)]
        self.mode = (1000, 820)
        self.gripper = 1

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
        self.blue = '#1F456E'
        self.em_1r_colour = self.black
        self.em_1l_colour = self.black
        self.em_2l_colour = self.black
        self.em_2r_colour = self.black

        self.em2r = False
        self.em2l = False
        self.em1r = False
        self.em1l = False

        #gripper image assets
        gripper_half = self.pygame.image.load(r'.\GUI Assets\Gripper  Half Open.png')
        self.gripper_half = self.pygame.transform.scale(gripper_half,(500,400))
        gripper_closed = self.pygame.image.load(r'.\GUI Assets\Gripper Closed.png')
        self.gripper_closed = self.pygame.transform.scale(gripper_closed,(500,400))
        gripper_full_opened =self.pygame.image.load(r".\GUI Assets\Gripper fully opened.png")
        self.gripper_full_opened = self.pygame.transform.scale(gripper_full_opened,(500,400))

        self.background = self.pygame.Surface(self.mode)
        self.background.fill(self.pygame.Color(self.turquoise))
        self.font = self.pygame.font.SysFont("Comic Sans MS", 30)
        self.active_tools = ("gamepad.gripper", "gamepad.EM1", "gamepad.EM2", "gamepad.erector")

        # pubsub init
        pub.subscribe(self.direct_handler, "gamepad.direct")
        pub.subscribe(self.gripper_handler,"gamepad.gripper")
        pub.subscribe(self.em_handler,"gamepad.em_states")

    def rect(self,colour, dimensions):
        self.pygame.draw.rect(self.screen, colour, self.pygame.Rect(dimensions))
        # (X coord, Y position from top, length, thickness)

    def em_back(self):
        # large rectangles
        self.rect(self.yellow, (100, 350, 200, 100))
        self.rect(self.blue, (400, 350, 200, 100))

        # top decorations
        self.rect(self.yellow, (120, 340, 50, 10))
        self.rect(self.yellow, (230, 340, 50, 10))

        self.rect(self.blue, (420, 340, 50, 10))
        self.rect(self.blue, (530, 340, 50, 10))

        self.triangle(self.em_1r_colour, [(230, 370), (230, 430), (270, 400)])
        self.triangle(self.em_2r_colour, [(530, 370), (530, 430), (570, 400)])
        self.triangle(self.em_1l_colour, [(170, 370), (170, 430), (130, 400)])
        self.triangle(self.em_2l_colour, [(470, 370), (470, 430), (430, 400)])

    def triangle(self, colour, points):
        self.pygame.draw.polygon(surface=self.screen, color=colour, points=points)

    def dcircle(self,colour, coords, size):
        self.pygame.draw.circle(self.screen, (colour), (coords), size)

    def plottings(self, point_x, point_y, offset_x, offset_y):
        coord_x = point_x * 80 + offset_x
        coord_y = point_y * -80 + offset_y
        self.dcircle((0, 200, 0), (coord_x, coord_y), 20)

    def dots_back(self):
        for i in range(4):
            self.dcircle((i * 50, i * 50, i * 50), (500, 200), 120 - i * 30)
            self.dcircle((i * 50, i * 50, i * 50), (200, 200), 120 - i * 30)

    # pubsub handler
    def direct_handler(self, message):
        self.movement = message["gamepad_direct"]

    def gripper_handler(self, message):
        self.gripper = message["tool_state"]

    def em_handler(self, message):
        self.em1l = message["gamepad.EM1L"]
        self.em1r = message["gamepad.EM1R"]
        self.em2l = message["gamepad.EM2L"]
        self.em2r = message["gamepad.EM2R"]

    def run(self):
        text = self.font.render(f"", False, (0,0,0))
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(text, (0,0))

        LLR, LUD, RLR, RUD,BL,BR = (self.movement)

        self.dots_back()
        self.plottings(LLR,-LUD,200,200)
        self.plottings(RLR,-RUD,500,200)

        self.em_back()
        print(self.gripper)

        if self.gripper == -1:
             self.screen.blit(self.gripper_full_opened,(-50,450))
        elif self.gripper == 0:
            self.screen.blit(self.gripper_half, (-50, 450))
        elif self.gripper == 1:
             self.screen.blit(self.gripper_closed, (-50, 450))


        if self.em1r == True:
            self.em_1r_colour = self.turquoise
        if self.em2r == True:
            self.em_2r_colour = self.turquoise
        if self.em1l == True:
            self.em_1l_colour = self.turquoise
        if self.em2l == True:
            self.em_2l_colour = self.turquoise
        if self.em2r == False:
            self.em_2r_colour = self.black
        if self.em2l == False:
            self.em_2l_colour = self.black
        if self.em1l == False:
            self.em_1l_colour = self.black
        if self.em1r == False:
            self.em_1r_colour = self.black


        #TODO Abstract Colours from the displayed items
        #Seperate the initialization
        #should be function(self)
        #self.function
        #Change to 1080p








