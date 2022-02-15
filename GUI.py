from ModuleBase import Module
from PyGameServices import PyGameServices
from pubsub import pub

class GUI(Module):
    def __init__(self):
        super().__init__()

        # variables
        self.movement = [0 for i in range(6)]
        self.mode = (1920,1080)
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


        #em backing colour
        self.em_1_colour = self.blue
        self.em_2_colour = self.yellow

        self.updown_colour = self.yellow

        self.em2r = False
        self.em2l = False
        self.em1r = False
        self.em1l = False

        self.profile = "A"
        self.invert = False


        #gripper image assets
        gripper_half = self.pygame.image.load(r'.\GUI Assets\Gripper  Half Open.png')
        self.gripper_half = self.pygame.transform.scale(gripper_half,(889,500))
        gripper_closed = self.pygame.image.load(r'.\GUI Assets\Gripper Closed.png')
        self.gripper_closed = self.pygame.transform.scale(gripper_closed,(889,500))
        gripper_full_opened =self.pygame.image.load(r".\GUI Assets\Gripper fully opened.png")
        self.gripper_full_opened = self.pygame.transform.scale(gripper_full_opened,(889,500))
        rov_upview = self.pygame.image.load(r".\GUI Assets\otodus_bottom_view.png")
        self.rov_upview = self.pygame.transform.scale(rov_upview,(400,400))

        self.background = self.pygame.Surface(self.mode)
        self.background.fill(self.pygame.Color(self.turquoise))
        self.comic_font_large = self.pygame.font.SysFont("Comic Sans MS", 160)
        self.comic_font_small = self.pygame.font.SysFont("Comic Sans MS", 40)
        self.active_tools = ("gamepad.gripper", "gamepad.EM1", "gamepad.EM2", "gamepad.erector")

        # pubsub init
        pub.subscribe(self.direct_handler, "gamepad.direct")
        pub.subscribe(self.gripper_handler,"gamepad.gripper")
        pub.subscribe(self.em_handler,"gamepad.em_states")
        pub.subscribe(self.profile_handler,"gamepad.profile")
        pub.subscribe(self.invert_handler,"gamepad.invert")

    def rect(self,colour, dimensions):
        self.pygame.draw.rect(self.screen, colour, self.pygame.Rect(dimensions))
        # (X coord, Y position from top, length, thickness)

    def em_back(self):
        # large rectangles
        self.rect(self.em_2_colour, (100, 350, 200, 100))
        self.rect(self.em_1_colour, (400, 350, 200, 100))

        # top decorations
        self.rect(self.em_2_colour, (120, 340, 50, 10))
        self.rect(self.em_2_colour , (230, 340, 50, 10))

        self.rect(self.em_1_colour, (420, 340, 50, 10))
        self.rect(self.em_1_colour, (530, 340, 50, 10))

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

    def updown(self, BLT, BRT):
        self.rect(self.yellow, (700, (450 + (-170 * (BLT + 1))), 50, ((BLT + 1) * 170)))
        self.rect(self.yellow, (800, (450 + (-170 * (BRT + 1))), 50, ((BRT + 1) * 170)))

    def dots_back(self):
        for i in range(4):
            self.dcircle((i * 50, i * 50, i * 50), (500, 200), 120 - i * 30)
            self.dcircle((i * 50, i * 50, i * 50), (200, 200), 120 - i * 30)


    def gripper_display(self):
        if self.gripper == -1:
             self.screen.blit(self.gripper_full_opened,(-100,450))
        elif self.gripper == 0:
            self.screen.blit(self.gripper_half, (-100, 450))
        elif self.gripper == 1:
             self.screen.blit(self.gripper_closed, (-100, 450))

    def em_activation(self):
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

    def updown_markers(self):
        self.rect(self.white, (700, 365, 50, 85))
        self.rect(self.black, (700, 280, 50, 85))
        self.rect(self.white, (700, 195, 50, 85))
        self.rect(self.black, (700, 110, 50, 85))

        self.rect(self.white, (800, 365, 50, 85))
        self.rect(self.black, (800, 280, 50, 85))
        self.rect(self.white, (800, 195, 50, 85))
        self.rect(self.black, (800, 110, 50, 85))

    # def rov_image(self):
    #     self.screen.blit(self.rov_upview, (1200, 50))

    def profile_label(self):
        self.rect(self.white, (1200, 540, 170, 170))
        self.profile_info = self.comic_font_large.render(str(self.profile), False, (0,0,0))
        self.screen.blit(self.profile_info,(1230,500))

    def inversion(self):
        self.inverting = self.comic_font_large.render(str(self.invert), False, (0,0,0))
        self.screen.blit(self.inverting,(1430,500))



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

    def profile_handler(self, message):
        self.profile = message["gamepad_profile"]

    def invert_handler(self, message):
        self.invert = message["gamepad_invert"]
    #x button to invert

    # MAIN LOOP
    def run(self):

        self.screen.blit(self.background, (0, 0))
        LLR, LUD, RLR, RUD,BL,BR = (self.movement)

        self.profile_label()
        self.dots_back()
        self.inversion()
        self.plottings(LLR,-LUD,200,200)
        self.plottings(RLR,-RUD,500,200)

        self.updown_markers()
        self.updown(BL,BR)
        self.gripper_display()
        self.em_back()
        self.em_activation()
        # self.rov_image()
        # print(self.invert)
        
        self.pygame.display.flip()
