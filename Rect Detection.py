import pygame 
import cv2

vid = cv2.VideoCapture(0)

running = True

while running == True:
    ret, frame = vid.read()
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord('t'):
        cv2.imwrite(r'.\GUI Assets\rect photo.jpeg', frame)

vid.release()
cv2.destroyAllWindows()
    
