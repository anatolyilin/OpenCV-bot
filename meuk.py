# from picamera.array import PiRGBArray
# from picamera import PiCamera
# import time
# import cv2
# import numpy as np
# from orblib import *
# # from matplotlib import pyplot as plt
#
#
# #
# # first = True
# # sift , kp1 , des1 = learnObject(True , 10)
# # while True:
# #     ist_kp2 = findObject(sift, kp1 , des1  , -1, OpenXwindowTimeout=20,show= True)
# #
#
# camera = PiCamera()
# # camera.resolution = (640, 480)
# camera.resolution = (1024, 768)
# camera.framerate = 10
# camera.vflip = True
# #rawCapture = PiRGBArray(camera, size=(640, 480))
# rawCapture = PiRGBArray(camera, size=(1024, 768))
# counter = 0
# time.sleep(0.2)
#
# # Initiate STAR detector
# orb = cv2.ORB_create(nfeatures=100000, scoreType=cv2.ORB_FAST_SCORE)
#
# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#     # grab the raw NumPy array representing the image, then initialize the timestamp
#     # and occupied/unoccupied text
#     image = frame.array
#
#     x1 = 260
#     y1 = 280
#     x2 = 450
#     # x2 = 380
#     y2 = 450
#     cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
#     imageROI = image[y1:y2, x1:x2]
#
#     img = cv2.cvtColor(imageROI, cv2.COLOR_BGR2GRAY)
#
#
#     # find the keypoints with ORB
#     kp1 = orb.detect(img,None)
#
#     # compute the descriptors with ORB
#     kp1, des1 = orb.compute(img, kp1)
#
#     # img2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     # kp2 = orb.detect(img2, None)
#     # kp2, des2 = orb.compute(img2, kp2)
#
#     rawCapture.truncate(0)
#     break
#
#
#
# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#     # grab the raw NumPy array representing the image, then initialize the timestamp
#     # and occupied/unoccupied text
#     image = frame.array
#
#     img2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # find the keypoints with ORB
#     kp2 = orb.detect(img2,None)
#
#     # compute the descriptors with ORB
#     kp2, des2 = orb.compute(img2, kp2)
#
#     bf = cv2.BFMatcher()
#     matches = bf.knnMatch(des1, des2, k=2)
#     print len(matches)
#
#     list_kp2 = []
#
#     # For each match...
#     for mat1, mat2 in matches:
#         (x2, y2) = (0, 0)
#         if mat1.distance < 0.75 * mat2.distance:
#             # good.append([mat1])
#             # Get the matching keypoints for each of the images
#             # img1_idx = mat1.queryIdx
#             # img2_idx = mat2.trainIdx
#             img2_idx = mat1.trainIdx
#             # x - columns
#             # y - rows
#             # Get the coordinates
#
#             (x2, y2) = kp2[img2_idx].pt
#             # Append to each list
#             list_kp2.append(x2)
#             cv2.circle(image, (int(x2), int(y2)), 3, (0, 255, 0), -1)
#
#     cv2.imshow("Frame", image)
#     key = cv2.waitKey(1)
#
#     rawCapture.truncate(0)
#
#
#


from orblib2 import *
print learnObject(show=False, counts=40)