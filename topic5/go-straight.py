import signal
import sys
import threading
import time

import board
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit as Kit

# CONSTANTS

PIN_FRONT_MOTOR = 17  # 11 -> 17
PWM_FREQ = 50
STEP = 15
THROTTLE_SLOW = 0.8
THROTTLE_STOP = 0
DC_LEFT = 5
DC_CENTER = 7.25
DC_RIGHT = 8.5


def signal_handler(signal, frame):
    kit.motor1.throttle = THROTTLE_STOP
    pwm.ChangeDutyCycle(DC_CENTER)
    time.sleep(0.3)
    GPIO.cleanup()
    sys.exit(0)


# INIT

signal.signal(signal.SIGINT, signal_handler)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_FRONT_MOTOR, GPIO.OUT)
pwm = GPIO.PWM(PIN_FRONT_MOTOR, PWM_FREQ)
pwm.start(DC_CENTER)
kit = Kit(i2c=board.I2C())  # pi hat v.5, M2 L+R-

# MAIN

pwm.ChangeDutyCycle(DC_CENTER)
kit.motor1.throttle = THROTTLE_SLOW

forever = threading.Event()
forever.wait()
