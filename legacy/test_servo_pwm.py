import RPi.GPIO as GPIO
import time
import curses

pwm = 0

def main(win):

    pin = 8
    zero_pos = 7.5
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)

    global pwm
    pwm = GPIO.PWM(pin, 50)
    pwm.start(zero_pos)

    pos = 0
    win.nodelay(True)
    key = ""
    win.clear()
    win.addstr("Detected key:")
    while 1:
        try:
            key = win.getkey()
            win.clear()
            win.addstr("[q:exit a: -0.5 d: +0.5 ] currently at :")
            win.addstr(str(pos))
            if str(key) == 'a':
                # win.addstr('left')
                pos -= 0.5
                pwm.ChangeDutyCycle(pos)
            elif str(key) == 'd':
                pos += 0.5
                pwm.ChangeDutyCycle(pos)
            elif str(key) =="q":
                GPIO.cleanup()
                quit()
            else:
                win.addstr(str(key))
        except Exception as e:
            # No input
            pass


curses.wrapper(main)
