import pygame
import cv2
import time

#Initialization
capture = cv2.VideoCapture(4)
success, camera_image = capture.read()

clock = pygame.time.Clock()
pygame.init()
event = pygame.event.get()
clock = pygame.time.Clock()
clock.tick(30)
reset = False
measure_taking = False
counters = 0
cal =  00000
slot = False
unused = False
measuring = False
counting = 0

black = (0,0,0)
blue = (0,0,100)
white = (255,255,255)

average = 0
N = 0
a = 0
b = 0
biomass = 0
whyyy = 0

display_surface = pygame.display.set_mode((1100,700))
pygame.display.set_caption('Basic Measurer')
font = pygame.font.Font(r'.\GUI Assets\comfortaa\Comfortaa-Bold.ttf', 37)
fonts = pygame.font.Font(r'.\GUI Assets\comfortaa\Comfortaa-Bold.ttf', 29)
fontss = pygame.font.Font(r'.\GUI Assets\comfortaa\Comfortaa-Bold.ttf', 19)

lengthtextrect = []

image1 = pygame.image.load(r'.\GUI Assets\test image1.jpeg')
image2 = pygame.image.load(r'.\GUI Assets\test image2.jpeg')
image3 = pygame.image.load(r'.\GUI Assets\test image3.jpeg')
imagers = [image1, image2, image3]
counter = 0
t=0
biomass_cal = False

length = [0,0,0 ]

buttcolor = [blue, black, black ]
slottext1 = font.render("0", True, white)
slottext2 = font.render("1", True, white)
slottext3 = font.render("2", True, white)
confirm  = font.render("Confirm", True, white)
slot_label = fonts.render("Choose Fish", True, black)

imagescale = 1.05
re_wid = 1
re_hei = 1

def imagerefresh():
    global imagers
    global image1
    global image2
    global image3
    global re_wid
    global re_hei
    image1 = pygame.transform.scale(image1, (int(640*imagescale),int(480*imagescale)))
    image2 = pygame.transform.scale(image2, (int(640*imagescale),int(480*imagescale)))
    image3 = pygame.transform.scale(image3, (int(640*imagescale),int(480*imagescale)))
    imagers = [image1, image2, image3]

length_text = ["0 Cm", "Fish 2: 0 cm", "Fish 3: 0 cm"]

def button_maker():
        global display_surface
        global mousey
        global mousex
        global buttcolor
        pygame.draw.rect(display_surface, buttcolor[0], [20*re_wid, 590*re_hei, 50,50])
        pygame.draw.rect(display_surface, buttcolor[1], [90*re_wid, 590*re_hei, 50,50])
        pygame.draw.rect(display_surface, buttcolor[2], [160*re_wid, 590*re_hei, 50,50])
        pygame.draw.rect(display_surface, black, [230*re_wid, 590*re_hei, 180,50])
        pygame.draw.rect(display_surface, white, [20*re_wid, 530*re_hei, 220,50])

        display_surface.blit(slottext1, (35*re_wid,600*re_hei))
        display_surface.blit(slottext2, (105*re_wid,600*re_hei))
        display_surface.blit(slottext3, (175*re_wid,600*re_hei))
        display_surface.blit(confirm, (240*re_wid, 600*re_hei))
        display_surface.blit(slot_label, (30*re_wid, 540*re_hei))

lengthtext1 = font.render(length_text[0], True, white)
lengthtext2 = font.render(length_text[1], True, white)
lengthtext3 = font.render(length_text[2], True, white)
lengthtext = [lengthtext1, lengthtext2, lengthtext3]
biomass_indicator = font.render(str(biomass), True, black)

keyref = fontss.render("W (Change Fish), A (take photo), S (Reset Reference), D (Measurement taking), E (Biomass Calculations)", True, black )
keyrefrect = keyref.get_rect()
keyrefrect.center = (540*re_wid, 670*re_hei)

subref = fontss.render("Press Confirm your choice of fish", True, black )
subrefrect = subref.get_rect()
subrefrect.center = (600*re_wid, 620*re_hei)


#this draws box around text
for i in range(3):
    lengthtextrect.append(lengthtext[i].get_rect())

#this provides position of text
for i in range(3):
    lengthtextrect[i].center = (700, 100 + 50*i)

def lengthtextrefresh():
    global t
    global lengthtext
    global length_text
    global lengthtext1
    global lengthtext2
    global lengthtext3
    global lengthtextrect

    lengthtext1 = font.render(length_text[0], True, black)
    lengthtext2 = font.render(length_text[1], True, black)
    lengthtext3 = font.render(length_text[2], True, black)
    lengthtext = [lengthtext1, lengthtext2, lengthtext3]
    for i in range(3):
        lengthtextrect[i] = (lengthtext[i].get_rect())
    for i in range(3):
        lengthtextrect[i].center = (900, 100 + 50 * i)

#this is the measuring part
def length_measure():
    global coords
    global t
    global length_ref
    global internal_reference
    ratio = float(length_ref[t]/internal_reference[t])
    new_length = (((coords[t][-1][0] - coords[t][-2][0]) ** 2) + ((coords[t][-1][1] - coords[t][-2][1]) ** 2)) ** 0.5
    cal= ratio * new_length
    return cal

#Camera Input
camera = cv2.VideoCapture(0)

#Default Reference length
length_ref = [9]*3

#Storage for coords
coords = [[[0,0],[0,0]],[[0,0],[0,0]],[[0,0],[0,0]]]

internal_reference = [10000000000000,1000000000000000,100000000000]
new_length = 100000

comic_font_small = pygame.font.SysFont("Comic Sans MS", 40)
runs = True
running = True
while running == True :
    click=pygame.mouse.get_pressed()
    mousex,mousey=pygame.mouse.get_pos()
    runs = True

    display_surface.fill(white)
    for event in pygame.event.get():
        width , height= pygame.display.get_surface().get_size()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            return_value, tv = camera.read()
            if t == 0:
                cv2.imwrite(r'.\GUI Assets\test image1.jpeg', tv)
                image1 = pygame.image.load(r'.\GUI Assets\test image1.jpeg')
            elif t == 1:
                cv2.imwrite(r'.\GUI Assets\test image2.jpeg', tv)
                image2 = pygame.image.load(r'.\GUI Assets\test image2.jpeg')
            elif t == 2:
                cv2.imwrite(r'.\GUI Assets\test image3.jpeg', tv)
                image3 = pygame.image.load(r'.\GUI Assets\test image3.jpeg')

        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #Fish Slot
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w :
            slot = True
            print("Running")
            print("w")

        elif slot == True:
            print("Selecting")
            if click[0] and 20*re_wid <= mousex <= 70*re_wid and 590*re_hei <= mousey <= 640*re_hei:
                t = 0
                buttcolor[0] = blue
                buttcolor[1] = black
                buttcolor[2] = black
            elif click[0] and 90*re_wid <= mousex <= 140*re_wid and 590*re_hei <= mousey <= 640*re_hei:
                t = 1
                buttcolor[1] = blue
                buttcolor[0] = black
                buttcolor[2] = black
            elif click[0] and 160*re_wid <= mousex <= 210*re_wid and 590*re_hei <= mousey <= 640*re_hei:
                t = 2
                buttcolor[2] = blue
                buttcolor[1] = black
                buttcolor[0] = black
            elif click[0] and 230*re_wid <= mousex <= 430*re_wid and 590*re_hei <= mousey <= 640*re_hei:
                slot = False
                print(slot)
                break

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            biomass_cal =True
            print("e")

        elif biomass_cal == True:
            biomass_cal = False
            a = float(input("Provide the value of a: "))
            b = float(input("Provide the value of b: "))
            N = float(input("Provide the value of N:"))
            biomass = round((N*a*(average**b)),3)

        #Resetting Reference
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            reset = True
            counter = 0
            print("s")

        elif reset == True and counter<2:
            print(reset)
            print(counter)
            if click[0] == True:
                coords[t].append((mousex, mousey))
                counter = counter + 1
            if counter == 2:
                internal_reference[t] = (((coords[t][-1][0] - coords[t][-2][0]) ** 2) + ((coords[t][-2][1] - coords[t][-1][1]) ** 2)) ** 0.5
                cal = 9
                reset = False
                counter+=1

        #Taking measurement
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            measure_taking = True
            counters = 0
            print("d")

        elif measure_taking == True :
            if click[0] == True and counters<2:
                coords[t].append((mousex, mousey))
                pygame.draw.line(display_surface, (white), coords[t][-1], coords[t][-2], 3)
                counters +=1
                print(counters)
            elif counters == 2 and measure_taking == True :
                cal = length_measure()
                length[t] = cal
                measure_taking == False

        #biomass calculations
        biomass_indicator = font.render(("Biomass: " + str(biomass)) + " Kg", True, black)
        biomass_rect = biomass_indicator.get_rect()
        biomass_rect.center = (900, 420)

        #Elements Refresh
        lengthtextrefresh()
        imagerefresh()
        length_text[t] = "Fish " + str(t + 1) + ": " + str(round(length[t], 3)) + " cm"

        #Display output
        for i in range(3):
            display_surface.blit(lengthtext[i], lengthtextrect[i])
        display_surface.blit(keyref, keyrefrect)
        display_surface.blit((imagers[t]), (0, 0))
        button_maker()

        display_surface.blit(biomass_indicator, biomass_rect)

        a_indicator = font.render(("A: " + str(a)), True, black)
        a_rect = a_indicator.get_rect()
        a_rect.center = (800, 350)
        display_surface.blit(a_indicator, a_rect)

        b_indicator = font.render(("B: "+ str(b)), True,  black)
        b_rect = b_indicator.get_rect()
        b_rect.center = (900, 350)
        display_surface.blit(b_indicator, b_rect)

        n_indicator = font.render(("N: "+ str(N)), True, black)
        n_rect = n_indicator.get_rect()
        n_rect.center = (1000, 350)
        display_surface.blit(n_indicator, n_rect)

        avg_indicator = font.render(("Average: "+ str(average) + "cm"), True, black)
        avg_rect = avg_indicator.get_rect()
        avg_rect.center = (900, 300)
        display_surface.blit(avg_indicator, avg_rect)
        display_surface.blit(subref, subrefrect)


        keyrefrect.center = (520 * re_wid, 670 * re_hei)
        average = round((float(sum(length)) / 3),3)
        biomass = round((N * a * (average ** b)), 3)

        if len(coords[t])>1:
            pygame.draw.line(display_surface, (white),coords[t][-1], coords[t][-2],3)
        pygame.display.flip()