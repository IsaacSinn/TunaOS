import pygame as pg
import cv2
import numpy as np

# default cam video cap and display
# rov cam is 720p (1280x720)
cap = cv2.VideoCapture(4)
fps = 60


screen_width = 1350
screen_height = 800
screen = pg.display.set_mode((screen_width, screen_height))
gray = (220, 220, 220)



rect1 = pg.image.load(r'.\GUI Assets\test image1.jpeg')
rect2 = pg.image.load(r'.\Photomosaic\image2.jpeg')
rect3 = pg.image.load(r'.\Photomosaic\image3.jpeg')
rect4 = pg.image.load(r'.\Photomosaic\image4.jpeg')
rect5 = pg.image.load(r'.\Photomosaic\image5.jpeg')
rect6 = pg.image.load(r'.\Photomosaic\image6.jpeg')
rect7 = pg.image.load(r'.\Photomosaic\image7.jpeg')
rect8 = pg.image.load(r'.\Photomosaic\image8.jpeg')

pair1 = pg.image.load(r'.\Photomosaic\pair1.jpeg')
pair2 = pg.image.load(r'.\Photomosaic\pair2.jpeg')
pair3 = pg.image.load(r'.\Photomosaic\pair3.jpeg')
pair4 = pg.image.load(r'.\Photomosaic\pair4.jpeg')


final_image = pg.image.load(r'.\Photomosaic\transect line.jpeg')


transect_line = [rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8]
pair = [pair1, pair2, pair3, pair4]

def draw_margin(picture):
    lx = 310
    rx = 330
    # left margin
    picture[0:480][lx] = (223, 115, 255)
    # right margin
    picture[0:480][rx] = (223, 115, 255)

# capture and crop
def capture_frame(row):
    global rect1
    global rect2
    global rect3
    global rect4
    global rect5
    global rect6
    global rect7
    global rect8

    if row == 1:
        return_value, frame = cap.read()
        leftcropped = frame[0:720, 0:740]
        rightcropped = frame[0:720, 600:1280]
        left_resize = cv2.resize(leftcropped, (325, 375))
        right_resize = cv2.resize(rightcropped, (325, 375))
        cv2.imwrite(r'.\Photomosaic\image1.jpeg', left_resize)
        cv2.imwrite(r'.\Photomosaic\image2.jpeg', right_resize)
        rect1 = pg.image.load(r'.\Photomosaic\image1.jpeg')
        rect2 = pg.image.load(r'.\Photomosaic\image2.jpeg')

    elif row == 2:
        return_value, frame = cap.read()
        leftcropped = frame[0:720, 0:740]
        rightcropped = frame[0:720, 600:1280]
        left_resize = cv2.resize(leftcropped, (325, 375))
        right_resize = cv2.resize(rightcropped, (325, 375))
        cv2.imwrite(r'.\Photomosaic\image3.jpeg', left_resize)
        cv2.imwrite(r'.\Photomosaic\image4.jpeg', right_resize)
        rect3 = pg.image.load(r'.\Photomosaic\image3.jpeg')
        rect4 = pg.image.load(r'.\Photomosaic\image4.jpeg')

    elif row == 3:
        return_value, frame = cap.read()
        leftcropped = frame[0:720, 0:740]
        rightcropped = frame[0:720, 600:1280]
        left_resize = cv2.resize(leftcropped, (325, 375))
        right_resize = cv2.resize(rightcropped, (325, 375))
        cv2.imwrite(r'.\Photomosaic\image5.jpeg', left_resize)
        cv2.imwrite(r'.\Photomosaic\image6.jpeg', right_resize)
        rect5 = pg.image.load(r'.\Photomosaic\image5.jpeg')
        rect6 = pg.image.load(r'.\Photomosaic\image6.jpeg')

    elif row == 4:
        return_value, frame = cap.read()
        leftcropped = frame[0:720, 0:740]
        rightcropped = frame[0:720, 600:1280]
        left_resize = cv2.resize(leftcropped, (325, 375))
        right_resize = cv2.resize(rightcropped, (325, 375))
        cv2.imwrite(r'.\Photomosaic\image7.jpeg', left_resize)
        cv2.imwrite(r'.\Photomosaic\image8.jpeg', right_resize)
        rect7 = pg.image.load(r'.\Photomosaic\image7.jpeg')
        rect8 = pg.image.load(r'.\Photomosaic\image8.jpeg')


# stitch
def stitch_frames():
    global final_image
    global pair1
    global pair2
    global pair3
    global pair4

    r1 = cv2.imread(r'.\Photomosaic\image1.jpeg')
    r2 = cv2.imread(r'.\Photomosaic\image2.jpeg')
    r3 = cv2.imread(r'.\Photomosaic\image3.jpeg')
    r4 = cv2.imread(r'.\Photomosaic\image4.jpeg')
    r5 = cv2.imread(r'.\Photomosaic\image5.jpeg')
    r6 = cv2.imread(r'.\Photomosaic\image6.jpeg')
    r7 = cv2.imread(r'.\Photomosaic\image7.jpeg')
    r8 = cv2.imread(r'.\Photomosaic\image8.jpeg')

    R1 = cv2.rotate(r1, cv2.ROTATE_90_CLOCKWISE)
    R2 = cv2.rotate(r2, cv2.ROTATE_90_CLOCKWISE)
    R3 = cv2.rotate(r3, cv2.ROTATE_90_CLOCKWISE)
    R4 = cv2.rotate(r4, cv2.ROTATE_90_CLOCKWISE)
    R5 = cv2.rotate(r5, cv2.ROTATE_90_CLOCKWISE)
    R6 = cv2.rotate(r6, cv2.ROTATE_90_CLOCKWISE)
    R7 = cv2.rotate(r7, cv2.ROTATE_90_CLOCKWISE)
    R8 = cv2.rotate(r8, cv2.ROTATE_90_CLOCKWISE)


    # stitch 4 pairs
    pair1 = np.vstack((R1, R2))
    pair2 = np.vstack((R3, R4))
    pair3 = np.vstack((R5, R6))
    pair4 = np.vstack((R7, R8))
    # cv2.imshow("p1", pair1)
    # cv2.imshow("p2", pair2)
    # cv2.imshow("p3", pair3)
    # cv2.imshow("p4", pair4)
    # four in one
    quad1 = np.hstack((pair1, pair2))
    quad2 = np.hstack((pair3, pair4))

    # cv2.imshow("quad1", quad1)
    # cv2.imshow("quad2", quad2)
    # final stitch
    final_image = np.hstack((quad1, quad2))
    cv2.imshow("Transect line", final_image)
    cv2.waitKey(0)


running = True
while running:
    success, img = cap.read()
    # draw_margin(img)
    display = cv2.resize(img, (640,480))
    cv2.imshow('Video', display)
    cv2.waitKey(fps)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                capture_frame(1)
                print("hm")
            if event.key == pg.K_2:
                capture_frame(2)
            if event.key == pg.K_3:
                capture_frame(3)
            if event.key == pg.K_4:
                capture_frame(4)
            if event.key == pg.K_s:
                stitch_frames()


    screen.fill(gray)
    screen.blit(rect1, (0, 0))
    screen.blit(rect2, (335, 0))
    screen.blit(rect3, (0, 400))
    screen.blit(rect4, (335, 400))
    screen.blit(rect5, (670, 0))
    screen.blit(rect6, (1005, 0))
    screen.blit(rect7, (670, 400))
    screen.blit(rect8, (1005, 400))
    pg.display.update()

