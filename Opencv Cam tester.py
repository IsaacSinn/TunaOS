import cv2 

cam_id = 0
vid = cv2.VideoCapture(cam_id)

while True:
    ret, frame = vid.read()
    cv2.imshow('Live feed', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('e'):
        cam_id +=1
        vid = cv2.VideoCapture(cam_id)
        print(cam_id)
        
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows