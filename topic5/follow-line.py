import signal
import sys
import time

import board
import cv2
import numpy as np
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit as Kit
from picamera2 import Picamera2

PIN_FRONT_MOTOR = 17  # 11 -> 17
PWM_FREQ = 50
STEP = 15
THROTTLE_SLOW = 0.8
THROTTLE_STOP = 0
DC_LEFT = 5
DC_RIGHT = 8.5
DC_CENTER = (DC_LEFT + DC_RIGHT) / 2
CROP_TOP = 0
CROP_BOTTOM = 160
CROP_LEFT = 0
CROP_RIGHT = 640 - CROP_LEFT
IDEAL_POS = (CROP_RIGHT - CROP_LEFT) / 2
LINE_NEAR = 0
LINE_FAR = 10


def signal_handler(signal, frame):
    picam2.stop()
    kit.motor1.throttle = THROTTLE_STOP
    pwm.ChangeDutyCycle(DC_CENTER)
    time.sleep(0.3)
    GPIO.cleanup()
    sys.exit(0)


def getDutyCycle(diff):
    # print(diff)
    if diff < -150:
        dc = DC_RIGHT
    elif diff < -0:
        dc = (DC_RIGHT + DC_CENTER) / 2
    elif diff > 0:
        dc = (DC_LEFT + DC_CENTER) / 2
    elif diff > 150:
        dc = DC_LEFT
    else:
        dc = DC_CENTER

    return dc


signal.signal(signal.SIGINT, signal_handler)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_FRONT_MOTOR, GPIO.OUT)
pwm = GPIO.PWM(PIN_FRONT_MOTOR, PWM_FREQ)
pwm.start(DC_CENTER)
kit = Kit(i2c=board.I2C())  # pi hat v.5, M2 L+R-
picam2 = Picamera2()
picam2.start()
next_duty_cycle = DC_CENTER
kit.motor1.throttle = THROTTLE_SLOW

farBackgroundCountPredict = 0

while True:
    im = picam2.capture_array()
    im = im[CROP_TOP:CROP_BOTTOM, CROP_LEFT:CROP_RIGHT]
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    for _ in range(3):
        im = cv2.GaussianBlur(im, (31, 31), 0)

    _, imThsh = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    farBackgroundCount = np.count_nonzero(imThsh[-10:])
    print(farBackgroundCountPredict - 1600, farBackgroundCount)
    if (farBackgroundCount < farBackgroundCountPredict - 1600):
        print('======')
        print('  ||  ')
        print(farBackgroundCountPredict, farBackgroundCount)
        signal_handler(0, 0)
    farBackgroundCountPredict += farBackgroundCountPredict + farBackgroundCount
    farBackgroundCountPredict //= 3

    imCanny = cv2.Canny(imThsh, 16, 255)
    nearEdges = np.argwhere(imCanny)[:, 1]
    if len(nearEdges) > 0:
        pos = np.mean(nearEdges)
    else:
        pos = IDEAL_POS

    diff = pos - IDEAL_POS

    next_duty_cycle = getDutyCycle(diff)
    pwm.ChangeDutyCycle(next_duty_cycle)
