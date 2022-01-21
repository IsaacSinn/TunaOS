from ModuleBase import Module
from PyGameServices import PyGameServices
from pubsub import pub

class GUI(Module):
    def __init__(self):
        super().__init__()

        # variables
        self.movement = [0 for i in range(6)]
        self.mode = (800, 800)
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
        pub.subscribe(self.gripper_handler,"gamepad.gripper")


    def em_back(self):
        #large rectangles
        rect(self.yellow,(100,350,200,100))
        rect(self.blue,(400,350,200,100))

        #top decorations
        rect(self.yellow,(120,340,50,10))
        rect(self.yellow,(230,340,50,10))

        rect(self.blue,(420,340,50,10))
        rect(self.blue,(530,340,50,10))

        #triangle
        triangle(self.black, [(230, 370), (230, 430), (270, 400)])
        triangle(self.black, [(530, 370), (530, 430), (570, 400)])
        triangle(self.black, [(170, 370), (170, 430), (130, 400)])
        triangle(self.black, [(470, 370), (470, 430), (430, 400)])



    # pubsub handler
    def direct_handler(self, message):
        self.movement = message["gamepad_direct"]

    def gripper_handler(self, message):
        self.gripper = message["tool_state"]


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
            #(X coord, Y position from top, length, thickness)

        def triangle(colour,points):
            self.pygame.draw.polygon(surface=self.screen, color=colour, points=points)


        def plottings(self, point_x, point_y, offset_x, offset_y):
            coord_x = point_x * 80 + offset_x
            coord_y = point_y * -80 + offset_y
            dcircle((0,200,0),(coord_x,coord_y),20)



        def em_active():
            print("OK")


        dots_back()
        plottings(LLR,-LUD,200,200)
        plottings(RLR,-RUD,500,200)

        self.em_back()
        print(self.gripper)

        #gripper image assets
        gripper_half = self.pygame.image.load(r'.\GUI Assets\Gripper  Half Open.png')
        gripper_half = self.pygame.transform.scale(gripper_half,(400,400))
        gripper_closed = self.pygame.image.load(r'.\GUI Assets\Gripper Closed.png')
        gripper_closed = self.pygame.transform.scale(gripper_closed,(400,4000))
        gripper_full_opened =self.pygame.image.load(r".\GUI Assets\Gripper fully opened.png")
        gripper_full_opened = self.pygame.transform.scale(gripper_full_opened,(400,400))

        # if self.gripper == -1:
        #     self.screen.blit(gripper_closed,(0,500))
        # elif self.gripper == 0:
        #     self.screen.blit(gripper_half, (0, 500))
        # elif self.gripper == 1:
        #     self.screen.blit(gripper_full_opened, (0, 500))

        self.screen.blit(gripper_full_opened, (0,500))
