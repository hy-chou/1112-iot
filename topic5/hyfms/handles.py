import signal
import sys
import time
import os

import board
import cv2
import numpy as np
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit as Kit
from picamera2 import Picamera2

from .constants import *


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


class Hyfms:
    def __init__(self):
        signal.signal(signal.SIGINT, self.handleExit)

        os.environ["LIBCAMERA_LOG_LEVELS"] = '2'
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_FRONT_MOTOR, GPIO.OUT)

        self.pwm = GPIO.PWM(PIN_FRONT_MOTOR, PWM_FREQ)
        self.kit = Kit(i2c=board.I2C())  # pi hat v.5, M2 L+R-
        self.picam2 = Picamera2()

        self.pwm.start(DC_CENTER)
        self.picam2.start()

    def handleExit(self, signum=None, frame=None):
        self.picam2.stop()
        self.kit.motor1.throttle = THROTTLE_STOP
        self.pwm.ChangeDutyCycle(DC_CENTER)
        time.sleep(1)
        GPIO.cleanup()
        sys.exit(0)

    def captureAndFilter(self):
        im = self.picam2.capture_array()
        im = im[CROP_TOP:CROP_BOTTOM, CROP_LEFT:CROP_RIGHT]
        im = cv2.GaussianBlur(im, (31, 31), 5)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)[:, :, 1]
        imGG = cv2.GaussianBlur(im, (31, 31), 5)
        _, imBinary = cv2.threshold(
            imGG, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        imEdge = cv2.Canny(imBinary, 16, 255)

        return imBinary, imEdge

    def isIntersection(self, imBinary):
        # stdGG = np.std(imGG)
        # print(f'std = {stdGG}')

        far_count = len(np.argwhere(imBinary[-10:])[:, 1])
        far_count_gain = far_count - self.far_count_predicted
        print(f'far count = {far_count}\tgain = {far_count_gain}')
        if far_count_gain > 900:
            return True
        self.far_count_predicted *= 3
        self.far_count_predicted += far_count
        self.far_count_predicted //= 4
        return False

    def negativeControl(self, imEdge):
        edges_near = np.argwhere(imEdge[5:15])[:, 1]
        if len(edges_near) > 0:
            pos = np.mean(edges_near)
            diff = pos - IDEAL_POS
            # print(f'diff = {diff}')
            next_duty_cycle = getDutyCycle(diff)
            self.pwm.ChangeDutyCycle(next_duty_cycle)
        # else:
        #     print('diff = N/A')

    def handleFollowLine(self):
        print('handleFollowLine() starting')

        self.kit.motor1.throttle = THROTTLE_SLOW

        self.far_count_predicted = 10 * (CROP_RIGHT - CROP_LEFT)
        while True:
            imBinary, imEdge = self.captureAndFilter()
            if (self.isIntersection(imBinary)):
                break
            self.negativeControl(imEdge)

        print('handleFollowLine() ended')

        self.kit.motor1.throttle = THROTTLE_STOP
        time.sleep(1)
