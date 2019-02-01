import serial
import cv2
import numpy as np
import os

import Main



ser = serial.Serial("COM6",9600)

def capturePhoto():
    while True:
        data = ser.readline()[:-2]  # the last bit gets rid of the new-line chars

        if data:

            camera = cv2.VideoCapture(0)
            while True:
                return_value, image = camera.read()
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                cv2.imshow('image', gray)
                if cv2.waitKey(1):
                    cv2.imwrite('test.jpg', image)
                    break
            camera.release()
            cv2.destroyAllWindows()
            Main.main()

capturePhoto()









