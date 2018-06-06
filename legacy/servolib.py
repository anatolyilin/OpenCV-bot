import RPi.GPIO as GPIO

pwm = 0
debug_info = 0
#zero_pos = 1.2 oude waarde
zero_pos = 7.5

def init_servo(pin=8,req_debug_info = 0, req_zero_pos = 7.5):
    GPIO.setmode(GPIO.BOARD)
    global debug_info
    debug_info = req_debug_info

    global zero_pos
    zero_pos = req_zero_pos

    GPIO.setup(pin, GPIO.OUT)
    global pwm
    pwm =GPIO.PWM(pin, 50)
    pwm.start(zero_pos)
    if debug_info == 1:
        print "Servo initialled on pin %d \n start postion is set to %f (default: 7.5) \n Call debug(False) to disable"  %(pin, zero_pos )

def moveto(posDeg, req_debug_info=0):
    pos = zero_pos + 0.05*posDeg
    pwm.ChangeDutyCycle(pos)
    if debug_info == 1 or req_debug_info == 1:
        print "Servo set on %f pos, based on start position %f (default: 7.5)" % (pos, zero_pos)

def debug(value = False):
    debug_info == 0
    if value:
        debug_info == 1

def cleanup():
    GPIO.cleanup()