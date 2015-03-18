import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)
fgbg = cv2.BackgroundSubtractorMOG()
# Define the codec and create VideoWriter object
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (320,240))
#avg = [[[0]*3]*240]*320

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,1)
        fgmask = fgbg.apply(frame)
        #out.write(frame)
        for x in range(0, 320):
            for y in range (0, 240):
                if fgmask[y][x] == 0:
                    frame[y][x] = [255, 0, 255]
        out.write(frame)
        cv2.imshow('frame',fgmask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
