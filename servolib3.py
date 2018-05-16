from RPIO import PWM
import pickle

servo =''
debug_info = 0
zero_pos = 0
zero_pos_man = 0
rico = 0
left_val = 0
right_val = 0

def fixround(digit):
    return round(digit/10)*10



def init_pickle(file ='servo.conf', req_debug_info = 0):
    global debug_info, zero_pos , rico, left_val, right_val, zero_pos_man , servo, pin
    debug_info = req_debug_info
    # [ rico , zero_pos, left_val, right_val , manual zero , pin ]
    with open(file, 'rb') as fp:
        listRead = pickle.load(fp)
    if listRead[4] != -1:
        zero_pos_man = listRead[4]
    else:
        zero_pos_man = listRead[1]
    zero_pos= listRead[1]
    pin = listRead[5]
    PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
    servo = PWM.Servo()
    servo.set_servo(pin, int(zero_pos))

    rico = listRead[0]
    left_val =listRead[2]
    right_val = listRead[3]



def init_servo(pin_req=14,req_debug_info = 0, req_zero_pos = 2400, left_val_req = 2400, right_val_req=1300):

    global debug_info, zero_pos, rico, left_val, right_val, zero_pos, servo, pin
    pin =pin_req
    debug_info = req_debug_info
    left_val = left_val_req
    right_val = right_val_req
    zero_pos = req_zero_pos
    rico = (right_val-left_val)/180
    servo = PWM.Servo()
    servo.set_servo(pin, int(zero_pos))

def moveto(posDeg, req_debug_info=0):
    global servo
    pos = -rico*posDeg + zero_pos
    servo.set_servo(pin, fixround(pos))

def debug(value = False):
    debug_info == 0
    if value:
        debug_info == 1
