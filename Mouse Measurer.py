import pygame
import cv2

pygame.init()
event = pygame.event.get()
clock = pygame.time.Clock()
clock.tick(120)
reset = False
measure_taking = False
counters = 0
cal =  666

image1 = pygame.image.load(r'.\GUI Assets\test image1.jpeg')
image2 = pygame.image.load(r'.\GUI Assets\test image2.jpeg')
image3 = pygame.image.load(r'.\GUI Assets\test image3.jpeg')
imagers = [image1, image2, image3]
counter = 0

def imagerefresh():
    global imagers
    global image1
    global image2
    global image3
    imagers = [image1, image2, image3]

length_text = ["No Value", "No Value", "No value"]

white = (150,150,150)
blue = (0,0,100)
black = (0,0,0)

#Initialization
display_surface = pygame.display.set_mode((1000,700))
pygame.display.set_caption('Basic Measurer')
font = pygame.font.Font('freesansbold.ttf', 35 )
fontss = pygame.font.Font('freesansbold.ttf', 20 )
t = 0
lengthtextrect = []

lengthtext1 = font.render(length_text[0], True, white, black)
lengthtext2 = font.render(length_text[1], True, white, black)
lengthtext3 = font.render(length_text[2], True, white, black)
lengthtext = [lengthtext1, lengthtext2, lengthtext3]

keyref = fontss.render("W (Change Slot), A (take photo), S (Reset Reference), D (Measurement taking) ", True, white, black )
keyrefrect = keyref.get_rect()
keyrefrect.center = (260, 500)

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
def length_measure(length_ref, internal_reference):
    global coords
    global t
    ratio = float(length_ref/internal_reference)
    new_length = (((coords[t][-1][0] - coords[t][-2][0]) ** 2) + ((coords[t][-1][1] - coords[t][-2][1]) ** 2)) ** 0.5
    cal= ratio * new_length
    return cal

#Camera Input
camera = cv2.VideoCapture(0)


#Default Reference length
length_ref = 10

#Storage for coords

coords = [[],[],[]]

internal_reference = 10000000000000
new_length = 100000000000000000000
measurement = 1000000000

comic_font_small = pygame.font.SysFont("Comic Sans MS", 40)

while True:
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

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            t = int(input("Choose new fish slot, 0, 1, 2"))

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            print("processing")
            reset = True
            counter = 0

        elif reset == True:
            if click[0] == True:
                print("taking reference")
                coords[t].append((mousex, mousey))
                counter = counter + 1
                print(counter)
            if counter > 1:
                print("entered")
                internal_reference = (((coords[t][-1][0] - coords[t][-2][0]) ** 2) + ((coords[t][-2][1] - coords[t][-1][1]) ** 2)) ** 0.5
                cal = 10
                reset = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            measure_taking = True

        elif measure_taking == True:
            if click[0] == True:
                coords[t].append((mousex, mousey))
                counters +=1
            if counters >2:
                cal = length_measure(length_ref, internal_reference)
                measure_taking == False

        lengthtextrefresh()
        imagerefresh()

        length_text[t] = str(round(cal, 6)) + "Cm"

        for i in range(3):
            display_surface.blit(lengthtext[i], lengthtextrect[i])

        display_surface.blit(keyref, keyrefrect)
        display_surface.blit((imagers[t]), (0, 0))
        if len(coords[t])>1:
            pygame.draw.line(display_surface, (white),coords[t][-1], coords[t][-2],3)
        pygame.display.flip()





