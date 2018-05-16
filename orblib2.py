from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np


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

    counter = 0
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        image = frame.array

        # just to show the object
        if counter < counts:
            # define ROI
            x1 = 260
            y1 = 280
            x2 = 450
            # x2 = 380
            y2 = 450
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
            imageROI = image[y1:y2, x1:x2]

            text = str(counter) + "/" + str(counts)
            cv2.putText(image, text, (10, 55), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255, 0), 4)

            counter += 1
        else:
            break

        if show:
            cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)

    # based on the last frame, learn
    img1 = cv2.cvtColor(imageROI, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(nfeatures=100000, scoreType=cv2.ORB_FAST_SCORE)
    kp = orb.detect(img1, None)
    kp1, des1 = orb.compute(img1, kp)

    if show:
        img2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kp2 = orb.detect(img2, None)
        kp2, des2 = orb.compute(img2, kp2)

        list_kp2, image = getKpList(des1, des2, kp2, image)

        cv2.imshow("Frame", image)
        key = cv2.waitKey(0) & 0xFF

    cv2.destroyAllWindows()
    camera.close()
    return orb, kp1, des1


def getKpList(des1, des2, kp2, image=0):
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    list_kp2 = []

    for mat1, mat2 in matches:
        if mat1.distance < 0.75 * mat2.distance:
            img2_idx = mat1.trainIdx
            (x2, y2) = kp2[img2_idx].pt
            list_kp2.append(x2)
            if not isinstance(image, int):
                cv2.circle(image, (int(x2), int(y2)), 3, (0, 255, 0), -1)
    return list_kp2, image

def findObject(orb, kp1, des1, iterations=1, warmup=0, show=False, computeHeading=False):

    angles = []
    list_kp2 = 0
    camera = PiCamera()
    # camera.resolution = (640, 480)
    camera.resolution = (1024, 768)
    camera.framerate = 5
    camera.vflip = True
    # rawCapture = PiRGBArray(camera, size=(640, 480))
    rawCapture = PiRGBArray(camera, size=(1024, 768))
    counter = 1
    time.sleep(0.1)
    bf = cv2.BFMatcher()

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array

        if warmup < counter:
            img2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            kp2 = orb.detect(img2, None)
            kp2, des2 = orb.compute(img2, kp2)

            list_kp2, image = getKpList(des1, des2, kp2, image)

            angles.append(decodeToAngle(list_kp2, res=1024))


        if show:
            cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF
            print decodeToAngle(list_kp2,res=1024)

        if iterations < counter and iterations > 0:
            break
        counter = counter + 1
        rawCapture.truncate(0)

    # cv2.destroyAllWindows()
    camera.close()

    angles = [x for x in angles if x != -1]
    if computeHeading:
        return list_kp2, str(np.median(angles))
    else:
        return list_kp2, str(-1)

def decodeToAngle(list_kp2, res=640):
    # 0 right, 180 left, 90 straight
    # find points histogram np.arange(3,7,2)
    # pixel 0 on the left, pixel 640 on the right
    # return hoek 0 on the right, 180 on the left.
    # with FOV of 53.5 deg, we can see grom 63.25 to 116.75 deg
    if len(list_kp2)>0:
        hist, _ = np.histogram(list_kp2[-1], np.arange(res), range=None, normed=False, weights=None,
                               density=None)
        x_val = np.argmax(hist)
        # inversed
        hoek = (53.5 / res) * x_val - 26.75

    # FOV is 53.5 deg!!!
        return hoek
    else:
        return -1