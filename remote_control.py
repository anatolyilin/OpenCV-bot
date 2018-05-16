import curses
from drive import *

def main(win):
    win.nodelay(True)
    win.clear()
    win.addstr("... Servo Position Calibration ... \n")
    while 1:
        try:
            win.clear()
            win.addstr(" WASD \n")
            key = win.getkey()
            if str(key) == 'w':
                slowFor()
            elif str(key) == 's':
                slowRev()
            elif str(key) == 'a':
                slowR()
            elif str(key) == 'd':
                slowL()

        except Exception as e:
            # No input
            pass

curses.wrapper(main)

