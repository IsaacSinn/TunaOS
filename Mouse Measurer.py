import pygame
import cv2

pygame.init()
event = pygame.event.get()
clock = pygame.time.Clock()
clock.tick(120)
reset = False
measure_taking = False
counters = 0
cal =  00000
slot = False
unused = False
measuring = False

white = (150,150,150)
blue = (0,0,100)
black = (0,0,0)

#Initialization

display_surface = pygame.display.set_mode((1000,700))
pygame.display.set_caption('Basic Measurer')
font = pygame.font.Font('freesansbold.ttf', 35 )
fonts = pygame.font.Font('freesansbold.ttf', 27)
fontss = pygame.font.Font('freesansbold.ttf', 20 )

lengthtextrect = []

image1 = pygame.image.load(r'.\GUI Assets\test image1.jpeg')
image2 = pygame.image.load(r'.\GUI Assets\test image2.jpeg')
image3 = pygame.image.load(r'.\GUI Assets\test image3.jpeg')
imagers = [image1, image2, image3]
counter = 0
t=0

length = [0,0,0 ]

buttcolor = [blue, black, black ]
slottext1 = font.render("0", True, white)
slottext2 = font.render("1", True, white)
slottext3 = font.render("2", True, white)
confirm  = font.render("Confirm", True, white)
slot_label = fonts.render("Choose Slots", True, white)

def imagerefresh():
    global imagers
    global image1
    global image2
    global image3
    imagers = [image1, image2, image3]

length_text = ["0 Cm", "Slot 1: 0 cm", "Slot 2: 0 cm"]

def button_maker():
        global display_surface
        global mousey
        global mousex
        global buttcolor
        pygame.draw.rect(display_surface, buttcolor[0], [20, 550, 50,50])
        pygame.draw.rect(display_surface, buttcolor[1], [90, 550, 50,50])
        pygame.draw.rect(display_surface, buttcolor[2], [160, 550, 50,50])
        pygame.draw.rect(display_surface, black, [230, 550, 160,50])
        pygame.draw.rect(display_surface, black, [20, 490, 200,50])

        display_surface.blit(slottext1, (35,560))
        display_surface.blit(slottext2, (105,560))
        display_surface.blit(slottext3, (175,560))
        display_surface.blit(confirm, (240, 560))
        display_surface.blit(slot_label, (30, 505))

lengthtext1 = font.render(length_text[0], True, white, black)
lengthtext2 = font.render(length_text[1], True, white, black)
lengthtext3 = font.render(length_text[2], True, white, black)
lengthtext = [lengthtext1, lengthtext2, lengthtext3]

keyref = fontss.render("W (Change Slot), A (take photo), S (Reset Reference), D (Measurement taking) ", True, white, black )
keyrefrect = keyref.get_rect()
keyrefrect.center = (400, 670)

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

    lengthtext1 = font.render(length_text[0], True, white, black)
    lengthtext2 = font.render(length_text[1], True, white, black)
    lengthtext3 = font.render(length_text[2], True, white, black)
    lengthtext = [lengthtext1, lengthtext2, lengthtext3]
    for i in range(3):
        lengthtextrect[i] = (lengthtext[i].get_rect())
    for i in range(3):
        lengthtextrect[i].center = (800, 100 + 50 * i)

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
coords = [[],[],[]]

internal_reference = [10000000000000,1000000000000000,100000000000]
new_length = [100000000000000000000]
measurement = 1000000000

comic_font_small = pygame.font.SysFont("Comic Sans MS", 40)

running = True
while running == True :
    click=pygame.mouse.get_pressed()
    mousex,mousey=pygame.mouse.get_pos()

    display_surface.fill(white)
    for event in pygame.event.get():
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

        elif slot == True:
            print("Selecting")
            if click[0] and 20 <= mousex <= 70 and 550 <= mousey <= 600:
                t = 0
                buttcolor[0] = blue
                buttcolor[1] = black
                buttcolor[2] = black
            elif click[0] and 90 <= mousex <= 140 and 550 <= mousey <= 600:
                t = 1
                buttcolor[1] = blue
                buttcolor[0] = black
                buttcolor[2] = black
            elif click[0] and 160 <= mousex <= 210 and 550 <= mousey <= 600:
                t = 2
                buttcolor[2] = blue
                buttcolor[1] = black
                buttcolor[0] = black
            elif click[0] and 230 <= mousex <= 430 and 550 <= mousey <= 600:
                slot = False
                print(slot)
                break

        #####################

        #Resetting Reference
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            reset = True
            counter = 0

        elif reset == True:
            print(reset)
            if click[0] == True and counter <2:
                coords[t].append((mousex, mousey))
                counter = counter + 1
            if counter == 2:
                internal_reference[t] = (((coords[t][-1][0] - coords[t][-2][0]) ** 2) + ((coords[t][-2][1] - coords[t][-1][1]) ** 2)) ** 0.5
                cal = 9
                reset = False
                break


        #########################

        #Taking measurement
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            measure_taking = True
            counters = 0
            print("entered")

        elif measure_taking == True:
            if click[0] == True and counters<2:
                coords[t].append((mousex, mousey))
                pygame.draw.line(display_surface, (white), coords[t][-1], coords[t][-2], 3)
                counters +=1
            elif counters == 2 and measure_taking == True :
                cal = length_measure()
                length[t] = cal
                measure_taking == False
                print("here")
                counters+=1
                break
                print("counters")

        #########################

        #Elements Refresh
        lengthtextrefresh()
        imagerefresh()
        length_text[t] = "Slot " + str(t)+ ": " + str(round(length[t], 3)) + " cm"

        #Display output
        for i in range(3):
            display_surface.blit(lengthtext[i], lengthtextrect[i])
        display_surface.blit(keyref, keyrefrect)
        display_surface.blit((imagers[t]), (0, 0))
        button_maker()
        if len(coords[t])>1:
            pygame.draw.line(display_surface, (white),coords[t][-1], coords[t][-2],3)
        pygame.display.flip()






