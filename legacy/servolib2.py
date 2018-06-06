import RPi.GPIO as GPIO
import pickle


pwm = 0
debug_info = 0
#zero_pos = 1.2 oude waarde
zero_pos = 0
zero_pos_man = 0
rico = 0
left_val = 0
right_val = 0


def init_pickle(file ='servo.conf', req_debug_info = 0):
    global debug_info, zero_pos , rico, left_val, right_val, zero_pos_man , pwm
    debug_info = req_debug_info
    # [ rico , zero_pos, left_val, right_val , manual zero , pin ]
    with open(file, 'rb') as fp:
        listRead = pickle.load(fp)
    if listRead[4] != -1:
        zero_pos_man = listRead[4]
    else:
        zero_pos_man = listRead[1]

    zero_pos= listRead[1]
    if debug_info == 1:
        print "Pickle data" + str(listRead)
    pin = listRead[5]

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50)
    pwm.start(zero_pos)
    rico = listRead[0]
    left_val =listRead[2]
    right_val = listRead[3]



def init_servo(pin=8,req_debug_info = 0, req_zero_pos = 7.5, left_val_req = 2, right_val_req=12.5):
    GPIO.setmode(GPIO.BOARD)
    global debug_info, zero_pos, rico, left_val, right_val, zero_pos, pwm
    debug_info = req_debug_info
    left_val = left_val_req
    right_val = right_val_req
    zero_pos = req_zero_pos
    rico = (right_val-left_val)/180
    GPIO.setup(pin, GPIO.OUT)
    pwm =GPIO.PWM(pin, 50)
    pwm.start(zero_pos)
    if debug_info == 1:
        print "Servo initialled on pin %d \n start postion is set to %f (default: 7.5) \n Call debug(False) to disable"  %(pin, zero_pos )

def moveto(posDeg, req_debug_info=0):
    pos = -rico*posDeg + zero_pos
    pwm.ChangeDutyCycle(pos)
    if debug_info == 1 or req_debug_info == 1:
        print "Servo set on %f pos, based on start position %f (default: 7.5)" % (pos, zero_pos)

def movetoZero():
    moveto(zero_pos_man)

def debug(value = False):
    debug_info == 0
    if value:
        debug_info == 1

def cleanup():
    GPIO.cleanup()