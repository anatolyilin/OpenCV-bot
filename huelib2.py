from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

from servolib3 import *
from drive import *
from distanceUltrasonic import *


def hsv_to_rgb(h, s, v):
    if s == 0.0: return [v, v, v]
    i = int(h * 6.)  # XXX assume int() truncates!
    f = (h * 6.) - i;
    p, q, t = 255 * v * (1. - s), 255 * v * (1. - s * f), 255 * v * (1. - s * (1. - f));
    i %= 6
    if i == 0: return [v, t, p]
    if i == 1: return [q, v, p]
    if i == 2: return [p, v, t]
    if i == 3: return [p, q, v]
    if i == 4: return [t, p, v]
    if i == 5: return [v, p, q]


def findLargestContour(contours):
    maxsize = 0
    return_contour = ''
    for i in contours:
        size = cv2.contourArea(i)
        if size > maxsize:
            maxsize = size
            return_contour = i
    return return_contour


def learnObject(show=True, counts=40):
    # initialize the camera and grab a reference to the raw camera capture
    kernel_size = 5
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 5
    camera.vflip = True
    rawCapture = PiRGBArray(camera, size=(640, 480))

    # counter = 90
    counter = 0

    # allow the camera to warmup
    time.sleep(0.1)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        if counter < counts:
            cv2.rectangle(image, (280, 200), (340, 280), (0, 255, 0), 3)
            # cv2.rectangle(image, (80,80) ,(240,240), (0,255,0),3 )
            # cv2.rectangle(image, (80,80) ,(110,110), (0,255,0),3 )
            # compute HSV, compute Hue
            # imageROI = image[80:140, 80:240]
            # imageROI = image[80:110, 80:110]
            imageROI = image[203:277, 283:337]

            imageROI_HSV = cv2.cvtColor(imageROI, cv2.COLOR_BGR2HSV)
            huechan = cv2.split(imageROI_HSV)
            histImg0 = cv2.calcHist(huechan, [0], None, [180], [0, 180])
            histImg1 = cv2.calcHist(huechan, [1], None, [256], [0, 256])
            histImg2 = cv2.calcHist(huechan, [2], None, [256], [0, 256])
            # histImg2, binEdges = numpy.histogram(huechan[0], 180, [0,180])
            minval, maxval, minloc, maxloc = cv2.minMaxLoc(histImg0)
            minval, maxval, minloc, maxloc1 = cv2.minMaxLoc(histImg1)
            minval, maxval, minloc, maxloc2 = cv2.minMaxLoc(histImg2)
            # use max color
            xvar, domcolor = maxloc
            xvar, domcolor1 = maxloc1
            xvar, domcolor2 = maxloc2
            print '----------------------------------------------'
            print hsv_to_rgb(domcolor * 2.0, domcolor1 / 256.0, domcolor2 / 256.0)
            text = str(counter) + "/" + str(counts)
            cv2.putText(image, text, (10, 55), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255, 0), 4)
            print '----------------------------------------------'
            counter = counter + 1
        else:
            break

        if show:
            cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF

        rawCapture.truncate(0)

    camera.close()
    cv2.destroyAllWindows()
    return [domcolor, domcolor1]


def findObject(domcolorArr, iterations=1, show=False, computeHeading=True):
    domcolor = domcolorArr[0]
    domcolor1 = domcolorArr[1]

    init_pickle()
    canny_1 = 20
    canny_2 = 40
    previous_angle = 0

    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 5
    camera.vflip = True
    rawCapture = PiRGBArray(camera, size=(640, 480))

    # counter = 90
    counter = 0

    # allow the camera to warmup
    time.sleep(0.1)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        hsvimage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # print "using ", domcolor
        huechan = cv2.split(hsvimage)
        mask1 = cv2.inRange(huechan[0], (domcolor - 10), (domcolor + 10))
        mask2 = cv2.inRange(huechan[1], (domcolor1 - 10), (domcolor1 + 10))
        mask = cv2.bitwise_and(mask1, mask1, mask=mask2)

        # edges = cv2.Canny(mask, canny_1, canny_2)

        _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        contours1 = findLargestContour(contours)
        if len(contours1) > 0:
            M = cv2.moments(contours1)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            # width, height = image.shape[:2]
            width = 480
            angle = (53.5 / 640) * cx - 26.75
            cv2.circle(image, (cx, cy), 10, (255, 255, 255), -1)
        else:
            angle = -1

        if show:
            cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF

        if iterations < counter and iterations > 0:
            break

        counter += 1
        rawCapture.truncate(0)

    camera.close()

    if computeHeading:
        return angle
    else:
        return contours1