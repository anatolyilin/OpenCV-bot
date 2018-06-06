import RPi.GPIO as GPIO
import pickle
import curses

pwm = 0
zero_pos_calib =[]
map_calib = []

def find_pos(win, text):
    pos = zero_pos
    GPIO.setwarnings(False)

    global pwm
    while 1:
        try:

            win.clear()
            win.addstr(text + " \n")
            win.addstr("q: exit \n a / d : -/+ 0.5 \n z/c: -/+ 0.05 \n p / enter: set \n")
            win.addstr("current value:")
            win.addstr(str(pos))
            key = win.getkey()
            if str(key) == 'q':
                GPIO.cleanup()
                quit()
            elif str(key) == 'a':
                pos -=0.5
                pwm.ChangeDutyCycle(pos)
            elif str(key) == 'z':
                pos -= 0.05
                pwm.ChangeDutyCycle(pos)
            elif str(key) == 'd':
                pos += 0.5
                pwm.ChangeDutyCycle(pos)
            elif str(key) == 'c':
                pos += 0.05
                pwm.ChangeDutyCycle(pos)
            elif str(key) == 'p' or str(key) == '':
                win.clear()
                win.addstr("set to "+ str(pos))
                return pos
        except Exception as e:
            # No input
            pass


def calib_zero(win):
    win.clear()
    text = "Place in the Zero / Dead center position"
    return find_pos(win, text)
def calib_LR(win):
    win.clear()
    left_text = "Place in the  Left position (w.r.t. driving direction) [+90 deg]"
    right_text = "Place in the  Right position (w.r.t. driving direction) [-90 deg]"
    left_val= find_pos(win, left_text)
    right_val=find_pos(win, right_text)
    rico = (right_val-left_val)/180.0
    zero_pos_val = right_val - rico*90.0
    return [rico, zero_pos_val,left_val,right_val]

def main(win):
    global pwm
    win.nodelay(True)
    global map_calib, zero_pos_calib
    win.clear()
    win.addstr("... Servo Position Calibration ... \n")
    win.addstr(
        " 1) calibrate L/R position of the servo [-90/+90 deg] \n 2) Calibrate Zero/ Dead center position \n q: exit \n s: save & quit \n")
    while 1:
        try:
            win.clear()
            win.addstr("... Servo Position Calibration ... \n")
            win.addstr(" 1) calibrate L/R position of the servo [-90/+90 deg] \n 2) Calibrate Zero/ Dead center position \n q: exit \n s: save & quit\n")

            win.addstr(" ============================================== \n")
            win.addstr("Zero pos | original: " + str(zero_pos) + " ,set manually: " + str(
            zero_pos_calib) + " ,calculated : " + str(map_calib[1]) + " \n")
            win.addstr("Map [ rico , zero_pos, left_val, right_val ]: [" + str(map_calib[0]) + " , " + str(
                map_calib[1]) + " , " + str(map_calib[2]) + " , " + str(map_calib[3]) + "] \n ")
            win.addstr(" ============================================== \n")
            key = win.getkey()
            if str(key) == '1':
                map_calib = calib_LR(win)
                # break
            elif str(key) == '2':
                zero_pos_calib = calib_zero(win)
                # break
            elif str(key) == 'q':
                GPIO.cleanup()
                quit()
            elif str(key) == 's':
                map_calib.append(zero_pos_calib)
                map_calib.append(pin)
                with open('servo.conf', 'wb') as fp:
                    pickle.dump(map_calib, fp)
                GPIO.cleanup()
                quit()
            else:
                win.addstr("choose 1 or 2, not "+ str(key))
        except Exception as e:
            # No input
            pass

load_settings = raw_input("Load Pickle [y/n]")
if load_settings == "y":
    with open('servo.conf', 'rb') as fp:
        listRead = pickle.load(fp)
    pin = int(listRead[5])

    zero_pos_calib = listRead[4]
    map_calib = [float(listRead[0]),float(listRead[1]),float(listRead[2]),float(listRead[3])]

    pin_input = raw_input("Servo pin [empty for read: "+ str(pin)+ "]: ")
    if pin_input != "":
        pin = int(pin_input)

    zero_input = raw_input("Zero Position estimation [empty for read "+ str(listRead[4])  + "]: ")
    if zero_input == "":
        zero_pos = float(listRead[4])
    else:
        zero_pos = float(zero_input)

else:

    zero_pos_calib ="-1"
    map_calib = [-1,-1,-1,-1]

    pin_input = raw_input("Servo pin [empty for default 8]: ")
    if pin_input == "":
        pin = 8
    else:
        pin = int(pin_input)

    zero_input = raw_input("Zero Position estimation [empty for default 7.5]: ")
    if zero_input == "":
        zero_pos = 7.5
    else:
        zero_pos = float(zero_input)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

pwm = GPIO.PWM(pin, 50)
pwm.start(zero_pos)

curses.wrapper(main)