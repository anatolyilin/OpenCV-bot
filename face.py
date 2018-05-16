import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 20
camera.vflip = True
rawCapture = PiRGBArray(camera, size=(640, 480))



# Create the haar cascade
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    # Capture frame-by-frame

    # Our operations on the frame come here
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    print("Found {0} faces!".format(len(faces)))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('frame', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    rawCapture.truncate(0)

# When everything done, release the capture

cv2.destroyAllWindows()
