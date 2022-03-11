import pygame
import cv2

pygame.init()

event = pygame.event.get()
image = pygame.image.load(r'.\GUI Assets\test image.jpeg')

white = (150,150,150)
display_surface = pygame.display.set_mode((480,480))
pygame.display.set_caption('Basic Measurer')

camera = cv2.VideoCapture(0)

coords = [(0,0), (0,0)]
this = True
internal_reference = 100000
new_length = 100000
measurement = 1000000

while True:
    click=pygame.mouse.get_pressed()
    mousex,mousey=pygame.mouse.get_pos()

    display_surface.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            return_value, tv = camera.read()
            cv2.imwrite(r'.\GUI Assets\test image.jpeg', tv)
            image = pygame.image.load(r'.\GUI Assets\test image.jpeg')
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if this == True:
            length_ref = int(input("Please give reference range"))
            print("Provide reference coord by clicking on the two points")
            this = False
        if len(coords) >=4:
            internal_reference = (((coords[3][0] - coords[2][0])**2) + ((coords[3][1] -coords[2][1])**2))**0.5



        if click[0] == True:
            coords.append((mousex, mousey))


        ratio = float(length_ref/internal_reference)
        new_length = (((coords[-1][0] - coords[-2][0]) ** 2) + ((coords[-1][1] - coords[-2][1]) ** 2)) ** 0.5
        cal= ratio * new_length
        print(cal)
        display_surface.blit(image, (0, 0))
        pygame.draw.line(display_surface, (white),coords[-1], coords[-2],3)
        pygame.display.flip()



