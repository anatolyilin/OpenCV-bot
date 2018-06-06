from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

canny_1 = 20
canny_2 = 40


# DELETE IT LATER1
# domcolor = 174

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
    return_contour = 1

    print contours

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

    if counter < 40:
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
        # show the frame
        # print(image)
        # print(minval, maxval, minloc, maxloc)
        # print(domcolor)
        # clear the stream in preparation for the next frame
        counter = counter + 1



    if counter >= 40:

        # image = cv2.medianBlur(image,9)
        hsvimage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # print "using ", domcolor
        huechan = cv2.split(hsvimage)
        mask = cv2.inRange(huechan[0], (domcolor - 10), (domcolor + 10))

        # kernel = np.ones((kernel_size,kernel_size),np.uint8)
        # mask = cv2.erode(mask,kernel,iterations = 1)

        # res = cv2.bitwise_and(image, image, mask= mask)

        edges = cv2.Canny(mask, canny_1, canny_2)
        # cv2.imshow("Frame", edges)
        # cv2.waitKey(0)
        min_line_length = 1
        max_line_grap = 1
        # image = edges


        # lines = cv2.HoughLinesP(mask, 1, np.pi / 180, 1)
        # print len(lines)
        # for line in lines:
        #     cv2.line(image, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, 255, 0), 1)



            # for rho,theta in lines[0]:
            # a = np.cos(theta)
            # b = np.sin(theta)
            # x0 = a*rho
            # y0 = b*rho
            # x1 = int(x0 + 1000*(-b))
            # y1 = int(y0 + 1000*(a))
            # x2 = int(x0 - 1000*(-b))
            # y2 = int(y0 - 1000*(a))

            # cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)

        # image = np.vstack((edges,edges2))

        ## canny approach, didn't work well
        ##edges = cv2.Canny(mask,100,200)
        ##image = edges

        ##im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        ## this one works ok
        im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

        ## fails
        ##cv2.drawContours(image, findLargestContour(contours), -1, (0,255,0), 3)
        contours1 = findLargestContour(contours)
        print len(contours1)

        # cv2.drawContours(image, contours1, -1, (0,255,0), 3)


        # min_val = domcolor - 20
        # max_val = domcolor + 20
        # red_lower = np.array([minval, 0, 0], np.uint8)
        # red_upper = np.array([maxval, 255, 255], np.uint8)
        # red_binary = cv2.inRange(huechan[0], red_lower, red_upper)
        # dilation = np.ones((15, 15), "uint8")
        # red_binary = cv2.dilate(red_binary, dilation)
        # im_res,  contours, hierarchy = cv2.findContours(red_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(image, contours, -1, (0,255,0), 3)

    # show the frame
    cv2.imshow("Frame", image)
    # # cv2.imshow("Frame", imageROI)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
