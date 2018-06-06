from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np


def findLargestContour(contours):
    maxsize = 0
    return_contour = ''
    for i in contours:
        size = cv2.contourArea(i)
        if size > maxsize:
            maxsize = size
            return_contour = i
    return return_contour


image = np.load("newimage2.npy")
domcolor  = 175
canny_1 = 20
canny_2 = 40
hsvimage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
huechan = cv2.split(hsvimage)
mask = cv2.inRange(huechan[0], (domcolor - 10), (domcolor + 10))
edges = cv2.Canny(mask, canny_1, canny_2)
im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours1 = findLargestContour(contours)

# cv2.drawContours(image, contours1, -1, (0,255,0), 3)

M = cv2.moments(contours1)
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
# width, height = image.shape[:2]
width = 480

angle = (cx-width/2)*(53.5/2)/(width/2)
print angle

cv2.circle(image,(cx,cy), 10, (255,255,255), -1)

cv2.imshow("Frame", image)
key = cv2.waitKey(0) & 0xFF