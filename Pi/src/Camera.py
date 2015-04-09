import numpy as np
import time
import cv2
import subprocess

NUM_FRAMES = 50
THRESHOLD = 30

class Camera:
    def recordVideo(self, name):
        cap = cv2.VideoCapture(0)
        cap.set(3, 480)
        cap.set(4, 480)
        #fgbg0 = cv2.BackgroundSubtractorMOG2()
        #time.sleep(1)
        #fgbg1 = cv2.BackgroundSubtractorMOG2()
        time.sleep(1)
        #fgbg2 = cv2.BackgroundSubtractorMOG2()
        #time.sleep(1)
        #fgbg3 = cv2.BackgroundSubtractorMOG()

        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        out = cv2.VideoWriter(name,fourcc, 20.0, (128,128))
        i = 0

        while(cap.isOpened()):
            ret, frame = cap.read()
            if i == 0:
                frame1 = frame
            if ret==True:
                diff = cv2.absdiff(frame, frame1)
                #frame = cv2.flip(frame,1)
                #frame = cv2.resize(frame, (128, 128), interpolation = cv2.INTER_AREA)
                #fgmask0 = fgbg0.apply(frame)
                #fgmask1 = fgbg1.apply(frame)
                #fgmask2 = fgbg2.apply(frame)
                #fgmask3 = fgbg3.apply(frame)

                #fg0 = cv2.bitwise_and(fgmask0, fgmask1)
                #fg1 = cv2.bitwise_and(fgmask0, fgmask2)
                #fg2 = cv2.bitwise_and(fgmask0, fgmask3)
                #fg3 = cv2.bitwise_and(fgmask1, fgmask2)
                #fg4 = cv2.bitwise_and(fgmask1, fgmask3)
                #fg5 = cv2.bitwise_and(fgmask2, fgmask3)
                #fgmask = fgmask0
                fgmask = cv2.inRange(diff, (THRESHOLD, THRESHOLD, THRESHOLD), (255,255,255))
                #fgmask = cv2.bitwise_or(fg0, fg1)
                #fgmask = cv2.bitwise_or(fgmask, fg2)
                #fgmask = cv2.bitwise_or(fgmask, fg3)
                #fgmask = cv2.bitwise_or(fgmask, fg4)
                #fgmask = cv2.bitwise_or(fgmask, fg5)

                frame = cv2.bitwise_and(frame, frame, mask = fgmask)
                frame = cv2.resize(frame, (128, 128), interpolation = cv2.INTER_CUBIC)
                frame = cv2.flip(frame, 1)
                cv2.imshow('frame',frame)
                frame = cv2.flip(frame, 0)
                image = cv2.imencode('.bmp', frame)
                imageName = name[0:4]
                imageName += '/'
                imageName += str(i)
                imageName += '.bmp'
                cv2.imwrite(imageName, frame)
                out.write(frame)
                i = i + 1
                if cv2.waitKey(1) & 0xFF == ord('q') or i == NUM_FRAMES:
                    break
            else:
                break

        # Release everything if job is finished
        cap.release()
        out.release()
        for i in range(5):
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        for i in range(5):
            cv2.waitKey(1)
