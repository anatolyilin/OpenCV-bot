from servolib3 import *

init_pickle(file ='servo.conf', req_debug_info = 1)
print "Input degree in range [-90 90] [R / L ]"
while 1:
    try:
        angle = raw_input("[q exit] Angle in degrees: ")
        if str(angle) == "q":
            break
        moveto(int(angle))
    except Exception as e:
        #No input
        pass

cleanup()