from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np


# test
# 1024, 768
def learnObject(show=True, counts=40):
    camera = PiCamera()
    # camera.resolution = (640, 480)
    camera.resolution = (1024, 768)
    camera.framerate = 10
    camera.vflip = True
    # rawCapture = PiRGBArray(camera, size=(640, 480))
    rawCapture = PiRGBArray(camera, size=(1024, 768))
    counter = 0
    time.sleep(0.1)
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        if counter < counts:
            # cv2.rectangle(image, (80,80) ,(240,140), (0,255,0),3 )
            # imageROI = image[80:140, 80:240]

            x1 = 260
            y1 = 280
            x2 = 450
            # x2 = 380
            y2 = 450
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
            imageROI = image[y1:y2, x1:x2]

            text = str(counter) + "/" + str(counts)
            cv2.putText(image, text, (10, 55), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255, 0), 4)
            counter = counter + 1
            # print counter, "/", counts, " complete"
        else:
            rawCapture.truncate(0)
            break
        if show:
            cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)

    img1 = cv2.cvtColor(imageROI, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(nfeatures=100000, scoreType=cv2.ORB_FAST_SCORE)
    kp = orb.detect(img1, None)

    # compute the descriptors with ORB
    kp1, des1 = orb.compute(img1, kp)

    img2 = cv2.drawKeypoints(img1,kp1,img1, color=(0,255,0), flags=0)
    cv2.imshow("Frame", img2)
    key = cv2.waitKey(0)

    # sift = cv2.xfeatures2d.SURF_create()
    # kp1, des1 = sift.detectAndCompute(img1, None)
    cv2.destroyAllWindows()
    camera.close()
    return orb, kp1, des1


def findObject(sift, kp1, des1, iterations=2, OpenXwindowTimeout= 20, show=False, computeHeading=False, printing=False):
    list_kp2 = 0
    camera = PiCamera()
    camera.resolution = (640, 480)
    # camera.resolution = (1024, 768)
    camera.framerate = 5
    camera.vflip = True
    rawCapture = PiRGBArray(camera, size=(640, 480))
    #rawCapture = PiRGBArray(camera, size=(1024, 768))
    counter = 0
    time.sleep(0.1)
    bf = cv2.BFMatcher()

    if show:
        OpenXwindowTimeout = OpenXwindowTimeout
        iterations = iterations+OpenXwindowTimeout+1
    else:
        OpenXwindowTimeout = 0


    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        if counter > OpenXwindowTimeout:
            if counter < iterations or iterations < 0:
                img2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                kp3 = sift.detect(img2, None)
                kp2, des2 = sift.compute(img2, kp3)
                # kp2, des2 = sift.detectAndCompute(img2, None)

                img3 = cv2.drawKeypoints(img2, kp3, img2, color=(0, 255, 0), flags=0)
                cv2.imshow("Frame", img3)
                key = cv2.waitKey(0)

                matches = bf.knnMatch(des1, des2, k=2)
                # good = []
                list_kp2 = []

                # For each match...
                for mat1, mat2 in matches:
                    (x2, y2) = (0, 0)
                    if mat1.distance < 0.75 * mat2.distance:
                        # good.append([mat1])
                        # Get the matching keypoints for each of the images
                        # img1_idx = mat1.queryIdx
                        # img2_idx = mat2.trainIdx
                        img2_idx = mat1.trainIdx
                        # x - columns
                        # y - rows
                        # Get the coordinates

                        (x2, y2) = kp2[img2_idx].pt
                        # Append to each list
                        list_kp2.append(x2)
                        if show:
                            cv2.circle(image, (int(x2), int(y2)), 3, (0, 255, 0), -1)
                            # image = cv2.drawMatchesKnn(image,kp1,img2,kp2,color=(0, 255, 0),flags=2)
                            # image = cv2.drawKeypoints(img1, kp1, img2, color=(0, 255, 0), flags=0)
                        if printing:
                            print list_kp2[-1]
                if computeHeading:
                    print "----- ", counter, " ------ "
                    print len(list_kp2)
                    # print decodeToAngle(list_kp2)
                    print "----- "
            else:
                rawCapture.truncate(0)
                break

        if show:
            cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF
            # key = cv2.waitKey(0)
        counter = counter + 1
        rawCapture.truncate(0)

    camera.close()
    return list_kp2


def decodeToAngle(list_kp2):
    # 0 right, 180 left, 90 straight
    # find points histogram np.arange(3,7,2)
    # pixel 0 on the left, pixel 640 on the right
    # return hoek 0 on the right, 180 on the left.
    # with FOV of 53.5 deg, we can see grom 63.25 to 116.75 deg
    if len(list_kp2)>0:
        hist, _ = np.histogram(list_kp2[-1], np.arange(640), range=None, normed=False, weights=None,
                               density=None)
        x_val = np.argmax(hist)
        # inversed
        hoek = (53.5 / 640) * x_val - 26.75
        # hoek = 63.25 + x_val * 53.5 / 640
    # hoek = 116.75 - x_val*53.5/640
    # FOV is 53.5 deg
        return hoek
    else:
        return -1