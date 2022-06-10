import cv2
import pygame 

cam_id = 1
#framerate and pygame screen
clock = pygame.time.Clock()
clock.tick(60)
pygame.display.init()
pygame.font.init()

res = (640, 700)
display = pygame.display.set_mode(res) 

#opencv camera
vid = cv2.VideoCapture(cam_id)

#colours
white = (255,255,255)
black = (0,0,0 )

#assets
rect_photo = pygame.image.load(r'.\GUI Assets\rect photo.jpeg')
rect_photo = pygame.transform.scale(rect_photo, (640, 360))

#reference size
ref = 33
ratio = float(1)
measured = float(1)

#keep track of process
ref_count = 0
ref_taking = False

mea_count = 0
mea_taking = False 

len_once = 0
.
#arrays for coords 
coords = [(50,50), (60,60)]
ref_coords = [(50,50), (60,60)]

#labels and fonts
fonts = pygame.font.Font(r'.\GUI Assets\comfortaa\Comfortaa-Bold.ttf', 15)

label = fonts.render("E (Measure || R (Draw Reference) || T (Take Pictures) || Y (Change ref value) ", True, white)
labelrect = label.get_rect()
labelrect.center = (300, 500)

measurement = fonts.render("Length" + str(measured), True, white)
measurementrect = measurement.get_rect()
measurementrect.center = (100, 550)


def pytha(x1, y1, x2, y2, ref):
    o_len = (((x2-x1)**2) + ((y2-y1) **2))**0.5
    ratio = float(ref/o_len)
    return ratio 

def pytha_cal(x1, y1, x2, y2):
    o_len = (((x2-x1)**2) + ((y2-y1) **2))**0.5
    return o_len

while True:
    ret, frame = vid.read()
    cv2.imshow('Live feed', frame)
    display.fill(black)

    for event in pygame.event.get():

        #End CV2 window 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        #Take photo
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            cv2.imwrite(r'.\GUI Assets\rect photo.jpeg', frame)
            rect_photo = pygame.image.load(r'.\GUI Assets\rect photo.jpeg')
            rect_photo = pygame.transform.scale(rect_photo, (640, 360))
            print("Taken Photo")

        #Take ref taking 
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            ref_count = 0 
            print("entered")
            ref_taking = True

        elif ref_taking == True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("position taken")
                ref_count+=1
                x, y = pygame.mouse.get_pos()
                ref_coords.append([x,y])

            elif ref_count >= 2:
                try:
                    ratio = pytha(ref_coords[-2][0], ref_coords[-2][1],ref_coords[-1][0], ref_coords[-1][1], ref)
                except ZeroDivisionError:
                    ratio = 0
                ref_taking = False

        #Taking Measurement 
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            mea_count = 0 
            print("entered")
            mea_taking = True

        elif mea_taking == True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("measure taking")
                mea_count+=1
                x, y= pygame.mouse.get_pos()
                coords.append([x,y])
            
            elif mea_count >= 2:
                len_once+=1
                measured = (pytha_cal(coords[-2][0], coords[-2][1],coords[-1][0],coords[-1][1]))*ratio 
                mea_taking = False

        #Change ref
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_y:
            ref = float(input("New Reference Value: "))

        display.blit(rect_photo, (0,0))
        display.blit(label, labelrect)
        display.blit(measurement, measurementrect)
        pygame.draw.line(display, black, ref_coords[-1], ref_coords[-2])
        pygame.draw.line(display, white, coords[-1], coords[-2])

        #length
        if len_once>0:
            print("Length measured",measured)
            measurement = fonts.render("Length" + str(measured), True, white)

        #refresh
        pygame.display.flip()

#program end
vid.release()
cv2.destroyAllWindows