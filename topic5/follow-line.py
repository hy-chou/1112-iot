import signal
import sys
import time

import board
import cv2
import numpy as np
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit as Kit
from picamera2 import Picamera2

# CONSTANTS

PIN_FRONT_MOTOR = 17  # 11 -> 17
PWM_FREQ = 50
STEP = 15
THROTTLE_SLOW = 0.8
THROTTLE_STOP = 0
DC_LEFT = 5
DC_CENTER = 7.25
DC_RIGHT = 8.5
CROP_TOP = 0
CROP_BOTTOM = 80
CROP_LEFT = 100
CROP_RIGHT = 640 - CROP_LEFT


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
picam2 = Picamera2()
picam2.start()


# MAIN

pwm.ChangeDutyCycle(DC_CENTER)
kit.motor1.throttle = THROTTLE_SLOW

while True:
    im = picam2.capture_array()
    im = im[CROP_TOP:CROP_BOTTOM, CROP_LEFT:CROP_RIGHT]

    im_b, im_g, im_r = im[:, :, 0], im[:, :, 1], im[:, :, 2]

    im_b = cv2.GaussianBlur(im_b, (5, 5), 0)
    im_g = cv2.GaussianBlur(im_g, (5, 5), 0)
    im_r = cv2.GaussianBlur(im_r, (5, 5), 0)
    _, im_b = cv2.threshold(im_b, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    _, im_g = cv2.threshold(im_g, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    _, im_r = cv2.threshold(im_r, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    im = np.logical_and(im_b, im_g)
    im = np.logical_and(im, im_r) * 255

    clear = np.std(im[0])
    # print(clear)

    offset = np.mean(np.nonzero(im[0])) - (CROP_RIGHT - CROP_LEFT)/2
    print(offset)
    if offset < -10:
        pwm.ChangeDutyCycle(DC_LEFT)
    elif offset > 10:
        pwm.ChangeDutyCycle(DC_RIGHT)
