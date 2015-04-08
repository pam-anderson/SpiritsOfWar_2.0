import numpy as np
import time
import cv2
import subprocess

def recordVideo(name):
    cap = cv2.VideoCapture(0)
    cap.set(3, 1920)
    cap.set(4, 1080)
    fgbg0 = cv2.BackgroundSubtractorMOG2()
    time.sleep(1)
    fgbg1 = cv2.BackgroundSubtractorMOG2()
    time.sleep(1)
    fgbg2 = cv2.BackgroundSubtractorMOG()
    time.sleep(1)
    fgbg3 = cv2.BackgroundSubtractorMOG2()

    #fgbg0 = cv2.resize(fgbg0, (128, 128), interpolation = cv2.INTER_AREA)
    #fgbg1 = cv2.resize(fgbg1, (128, 128), interpolation = cv2.INTER_AREA)
    #fgbg2 = cv2.resize(fgbg2, (128, 128), interpolation = cv2.INTER_AREA)
    #fgbg3 = cv2.resize(fgbg3, (128, 128), interpolation = cv2.INTER_AREA)

    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    out = cv2.VideoWriter(name,fourcc, 20.0, (128,128))
    i = 0

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            frame = cv2.flip(frame,1)
            frame = cv2.resize(frame, (128, 128), interpolation = cv2.INTER_AREA)
            fgmask0 = fgbg0.apply(frame)
            fgmask1 = fgbg1.apply(frame)
            fgmask2 = fgbg2.apply(frame)
            fgmask3 = fgbg3.apply(frame)

            #fgmask0 = cv2.resize(fgmask0, (128, 128), interpolation = cv2.INTER_AREA)
            #fgmask1 = cv2.resize(fgmask1, (128, 128), interpolation = cv2.INTER_AREA)
            #fgmask2 = cv2.resize(fgmask2, (128, 128), interpolation = cv2.INTER_AREA)
            #fgmask3 = cv2.resize(fgmask3, (128, 128), interpolation = cv2.INTER_AREA)

            fg0 = cv2.bitwise_and(fgmask0, fgmask1)
            fg1 = cv2.bitwise_and(fgmask0, fgmask2)
            fg2 = cv2.bitwise_and(fgmask0, fgmask3)
            fg3 = cv2.bitwise_and(fgmask1, fgmask2)
            fg4 = cv2.bitwise_and(fgmask1, fgmask3)
            fg5 = cv2.bitwise_and(fgmask2, fgmask3)
            fgmask = cv2.bitwise_or(fg0, fg1)
            fgmask = cv2.bitwise_or(fgmask, fg2)
            fgmask = cv2.bitwise_or(fgmask, fg3)
            fgmask = cv2.bitwise_or(fgmask, fg4)
            fgmask = cv2.bitwise_or(fgmask, fg5)
            #fgmask0 = fgbg0.apply(frame)
            #fgmask1 = fgbg1.apply(frame)
            #fgmask = cv2.bitwise_xor(fgmask0, fgmask1)
            #fgmask = cv2.resize(fgmask, (128, 128), interpolation = cv2.INTER_AREA)
            frame = cv2.bitwise_and(frame, frame, mask = fgmask)
            out.write(frame)
            cv2.imshow('frame',frame)
            i = i + 1
            if cv2.waitKey(1) & 0xFF == ord('q') or i == 60:
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def sendVideo(name):
    cap = cv2.VideoCapture(name)
    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        image = cv2.imencode('.bmp', frame)
        cv2.imwrite('frame.bmp', frame)
        subprocess.call(['sudo','./pins'])
        i = i + 1
        if cv2.waitKey(1) & 0xFF == ord('q') or i == 20:
            break
    cap.release()
    cv2.destroyAllWindows()
        
sendVideo('test.avi')



