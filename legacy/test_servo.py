from servolib import *
import time
import curses

def main(win):
    init_servo(8)
    pos = 0
    win.nodelay(True)
    key = ""
    win.clear()
    win.addstr("Detected key:")
    while 1:
        try:
            key = win.getkey()
            win.clear()
            win.addstr("[q:exit a:-10 d:+10 ] currently at :")
            win.addstr(str(pos))
            if str(key) == 'a':
                # win.addstr('left')
                pos -= 10
                moveto(pos)
            elif str(key) == 'd':
                pos += 10
                moveto(pos)
            elif str(key) =="q":
                cleanup()
                quit()
            else:
                win.addstr(str(key))
        except Exception as e:
            # No input
            pass


curses.wrapper(main)
