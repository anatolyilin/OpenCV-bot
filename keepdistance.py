#!/usr/bin/env python
# coding: Latin-1

# Simple example of a motor sequence script

# Import library functions we need
import PicoBorgRev
import time
from distanceUltrasonic import *
# Setup the PicoBorg Reverse
PBR = PicoBorgRev.PicoBorgRev()     # Create a new PicoBorg Reverse object
PBR.Init()                          # Set the board up (checks the board is connected)
PBR.ResetEpo()                      # Reset the stop switch (EPO) state


speed  =0.9

distanceLimit = int(raw_input("distance [cm]: "))


# fix wiring fail
def SetMotors(pwr):
    PBR.SetMotor1(pwr)
    PBR.SetMotor2(pwr)
try:
    while 1:
        distance = measuredist()
        print distance
        if (distance >  distanceLimit):
            SetMotors(speed)
        else:
            SetMotors(-speed)

    # PBR.SetMotor1(step[0])                  # Set the first motor to the first value in the pair
    # PBR.SetMotor2(step[1])                  # Set the second motor to the second value in the pair
    # print '%+.1f %+.1f' % (step[0], step[1])
    # time.sleep(stepDelay)                   # Wait between steps

    #GetDriveFault(self): SetMotors(self, power):

except KeyboardInterrupt:
    # User has pressed CTRL+C
    PBR.MotorsOff()                 # Turn both motors off
