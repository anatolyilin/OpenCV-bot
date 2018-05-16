from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

camera = PiCamera()
camera.resolution =  (1024, 768)
camera.framerate = 10
camera.vflip = True
rawCapture = PiRGBArray(camera, size= (1024, 768))
counter = 0
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    x1 = 260
    y1 = 280
    x2 = 450
    # x2 = 380
    y2 = 450
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
    imageROI = image[y1:y2, x1:x2]
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
camera.close()