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
CROP_AREA = (CROP_BOTTOM - CROP_TOP) * (CROP_RIGHT - CROP_LEFT)
IDEAL_POS = (CROP_RIGHT - CROP_LEFT) / 2
LINE_NEAR = 0
LINE_FAR = 10
SLEEP_TIME_90 = 3.2
SLEEP_TIME_45 = 1.6


def handleExit(signal=None, frame=None):
    picam2.stop()
    kit.motor1.throttle = THROTTLE_STOP
    pwm.ChangeDutyCycle(DC_CENTER)
    time.sleep(0.3)
    GPIO.cleanup()
    sys.exit(0)


def handleIntersection():
    handleExit()


def getDutyCycle(diff):
    if diff < -150:
        dc = DC_RIGHT
    elif diff < -100:
        dc = (DC_RIGHT * 2 + DC_CENTER) / 3
    elif diff < 0:
        dc = (DC_RIGHT + DC_CENTER * 2) / 3
    elif diff < 100:
        dc = (DC_LEFT + DC_CENTER * 2) / 3
    elif diff < 150:
        dc = (DC_LEFT * 2 + DC_CENTER) / 3
    else:
        dc = DC_LEFT

    return dc


signal.signal(signal.SIGINT, handleExit)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_FRONT_MOTOR, GPIO.OUT)
pwm = GPIO.PWM(PIN_FRONT_MOTOR, PWM_FREQ)
pwm.start(DC_CENTER)
kit = Kit(i2c=board.I2C())  # pi hat v.5, M2 L+R-
picam2 = Picamera2()
picam2.start()
next_duty_cycle = DC_CENTER
kit.motor1.throttle = THROTTLE_SLOW


print('starting sleep')
time.sleep(SLEEP_TIME_45)
pwm.ChangeDutyCycle(DC_RIGHT)
time.sleep(SLEEP_TIME_45)
pwm.ChangeDutyCycle((DC_RIGHT * 2 + DC_CENTER) / 3)
print('ending sleep')

while True:
    # Capture and Filter
    im = picam2.capture_array()
    im = im[CROP_TOP:CROP_BOTTOM, CROP_LEFT:CROP_RIGHT]
    im = cv2.GaussianBlur(im, (31, 31), 5)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)[:, :, 1]
    imGG = cv2.GaussianBlur(im, (31, 31), 5)
    _, imBinary = cv2.threshold(
        imGG, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    # imEdge = cv2.Canny(imBinary, 16, 255)

    stdGG = np.std(imGG)
    print(f'std = {stdGG}')
    if stdGG > 10:
        handleExit()
