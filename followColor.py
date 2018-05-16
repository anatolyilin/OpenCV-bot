from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np


canny_1 = 20
canny_2 = 40

type = int(raw_input("1: Ranger following [sudo!] 2: Follow car 3: Drive up-to [1-3] "))
if int(type) == 1:
    from servolib3 import *
    init_pickle()
elif int(type) == 2:
    from drive import *
elif int(type) == 3:
    from servolib3 import *
    from drive import *
    from distanceUltrasonic import *
    # distanceLimit = int(raw_input(" Drive up to [cm]: "))
    # speed = float(raw_input(" Speed [0.2 - 1.0 (% power)]: "))
    distanceLimit = 10
    speed = 0.3
    init_pickle()
else:
    print("1 to 3..., not "+ str(type))
    quit()
previous_angle = 0

def updateposition(angle):
    print angle
    command =[0 , 0]
    distance = measuredist()
    if abs(angle) > 1:
        if angle > 0:
            command[0] -= 0.25
            command[1] += 0.25
        else:
            command[0] += 0.25
            command[1] -= 0.25
    if abs(distance - distanceLimit) > 2:
        if (distance - distanceLimit) > 40:
            speed2 = 0.8
        else:
            speed2 = 0.2

        if (distance > distanceLimit):
            command[0] += speed2
            command[1] += speed2
        else:
            command[0] -= speed2
            command[1] -= speed2
    DriveMotors(command, 0.10*abs(angle))

def drive():
    distance = measuredist()
    if abs(distance - distanceLimit) > 2:
        if (distance - distanceLimit) > 40:
            speed2 = 0.8
        else:
            speed2 =0.2
        if (distance > distanceLimit) :
            SetMotors(speed2)
        else:
            SetMotors(-speed2)


def moveCar(angle):
    if abs(angle) > 1:
        if angle > 0:
            slowL(0.10*abs(angle))
        else:
            slowR(0.10*abs(angle))

def moveServ(angle):
    global previous_angle

    if abs(angle - previous_angle) > 5:
        previous_angle = angle
        moveto(angle)

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

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    if counter < 20:
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
        print domcolor, domcolor1, domcolor2
        print hsv_to_rgb(domcolor * 2.0, domcolor1 / 256.0, domcolor2 / 256.0)
        print '----------------------------------------------'
        counter = counter + 1

    if counter >=20 :

        hsvimage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # print "using ", domcolor
        huechan = cv2.split(hsvimage)
        mask = cv2.inRange(huechan[0], (domcolor - 10), (domcolor + 10))
        edges = cv2.Canny(mask, canny_1, canny_2)

        _, contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

        contours1 = findLargestContour(contours)
        if len(contours1) > 0:
            M = cv2.moments(contours1)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            # width, height = image.shape[:2]
            width = 480

            angle = (53.5/640)*cx - 26.75

            if int(type) == 1:
                moveServ(angle)
            elif int(type)==2:
                moveCar(angle)
            elif int(type)==3:
                 moveServ(angle)
                 moveCar(angle)
                 drive()
                 # updateposition(angle)

            cv2.circle(image, (cx, cy), 10, (255, 255, 255), -1)

    # show the frame
    cv2.imshow("Frame", image)
    # # cv2.imshow("Frame", imageROI)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
