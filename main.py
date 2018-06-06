from servolib3 import *
from drive import *
from distanceUltrasonic import *
import numpy as np
previous_angle = 0
actions =[]
state = 'none'

def updateposition(angle, distanceLimit, thresAngle = 1, thresholdDistance=2):
    print angle
    command =[0 , 0]
    distance = measuredist()
    if abs(angle) > thresAngle:
        if angle > 0:
            command[0] -= 0.25
            command[1] += 0.25
        else:
            command[0] += 0.25
            command[1] -= 0.25
    if abs(distance - distanceLimit) > thresholdDistance:
        if (distance > distanceLimit):
            command[0] += 0.20
            command[1] += 0.20
        else:
            command[0] -= 0.20
            command[1] -= 0.20
    DriveMotors(command, 0.10*abs(angle))
def drive(speed, distanceLimit, threshold=2):
    distance = measuredist()
    if speed == "auto":
        if (distance - distanceLimit) > 40:
            speed = 0.8
        else:
            speed = 0.2

    if abs(distance - distanceLimit) > threshold:
        if (distance > distanceLimit) :
            SetMotors(speed)
        else:
            SetMotors(-speed)
def moveCar(angle2):
    if abs(angle2) > 1:
        if angle2 > 0:
            slowL(0.10*abs(angle2))
        else:
            slowR(0.10*abs(angle2))
def moveServ(angle3):
    init_pickle()
    global previous_angle
    if abs(angle3 - previous_angle) > 5:
        previous_angle = angle3
        moveto(angle3)
def notfound():
    moveServ(0)
    global state, actions, distanceLimit, speed
    if len(actions) == 0:
        state ="scan"
        actions.append("R")
        print "first time object not found, first scan Right"
        moveCar(-90)
    else:
        if state == "scan":
            if actions[-1] == "R":
                actions.append("C")
                print "scanned right, now scan center"
                moveCar(90)
                drive(-speed, distanceLimit)
            elif actions[-1] == "C":
                actions.append("L")
                print "scanned center, now scan left"
                moveCar(90)
            elif actions[-1] == "L":
                state ="drive"
                print "scanned left, nothing found, so drive!"

                if measuredist() > distanceLimit:
                    moveCar(-90)
                    drive(speed, distanceLimit)
                else:
                    print  "not enough space to drive forward, try right!"
                    moveServ(-90)
                    if measuredist() > distanceLimit:
                        # enough space on the right!
                        moveCar(-90)
                        drive(speed, distanceLimit)
                    else:
                        print "not enough spance on the right.."
                        moveServ(90)
                        if measuredist() > distanceLimit:
                            print  "enough space on the left!"
                            moveCar(90)
                            drive(speed, distanceLimit)
                        else:
                            print "not enough space on the left, let's try to turn around"
                            moveServ(0)
                            moveCar(-180)

        else:
            print "state is drive, so we scanned R->L then drove. So let's restart"
            actions = []
            state == "scan"
            notfound()
    return 1
# Determine
type = int(raw_input("1: Hue, 2: Sift, 3: ORB [1-3]: "))

if int(type) == 1:
    from huelib2 import *
elif int(type) == 2:
    from siftlib import *
elif int(type) == 3:
    from orblib2 import *
else:
    print "Unknown choice"

distanceLimit = 10
    # int(raw_input("Distance limit [cm]: "))
speed =  0.2
    # float(raw_input("Power [ 0.2-1.0 % ]: "))


# Learn Object
if int(type) == 1:
    obj = learnObject(True,20)
else:
    obj , kp1 , des1 = learnObject(True, 40)

# Follow
notFound = 0
while True:
    dirangle = -1
    if int(type) == 1:
        dirangle = findObject(obj, iterations=1, show=True, computeHeading=True)
    else:
        _, dirangle =findObject(obj, kp1, des1, iterations=1, show=True, computeHeading=True)
    if dirangle != -1:
        notFound = 0
        actions = []
        state = 'none'
        moveServ(float(dirangle))
        # updateposition(direction, distanceLimit)
        moveCar(float(dirangle))
        drive("auto", distanceLimit, threshold=2)
    elif notFound == 0:
        print "not found... "
        notFound += 0
    else:
        print "object not found. #" + str(notFound)
        # rules:
        # try to go straight (if possible, otherwise detect direction) -> scan -> not found -> rotate right -> scan -> not found -> rotate left (2x) -> scan
        notfound()

    print dirangle

