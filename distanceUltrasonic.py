import RPi.GPIO as GPIO
import time


def measuredist(pin=11):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(pin, True)
    time.sleep(5 / 1000000.0)
    # time.sleep(0.00001)GPIO.output(pin, False)
    GPIO.setup(pin, GPIO.IN)

    while GPIO.input(pin) == 0:
        signaloff = time.time()

    while GPIO.input(pin) == 1:
        signalon = time.time()

    while GPIO.input(pin) == 1:
        signalon = time.time()

    duration = signalon - signaloff
    # distance = duration * 17000
    distance = duration / 29 / 2 * 1000000
    return distance