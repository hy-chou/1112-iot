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
        dc = DC_R3
    elif diff < -100:
        dc = DC_R2
    elif diff < 0:
        dc = DC_R1
    elif diff < 100:
        dc = DC_L1
    elif diff < 150:
        dc = DC_L2
    else:
        dc = DC_L3

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
        self.motorStop()
        # self.pwm.ChangeDutyCycle(DC_CENTER)
        time.sleep(1)
        GPIO.cleanup()
        sys.exit(0)

    def motorRun(self):
        self.kit.motor1.throttle = THROTTLE_SLOW

    def motorStop(self):
        self.kit.motor1.throttle = THROTTLE_STOP

    def __captureAndFilter(self):
        self.im = self.picam2.capture_array()
        self.imCrop = self.im[CROP_TOP:CROP_BOTTOM, CROP_LEFT:CROP_RIGHT]
        self.imBlur = cv2.GaussianBlur(self.imCrop, (31, 31), 5)
        self.imSat = cv2.cvtColor(self.imBlur, cv2.COLOR_BGR2HSV)[:, :, 1]
        self.imBlurBlur = cv2.GaussianBlur(self.imSat, (31, 31), 5)
        _, self.imBinary = cv2.threshold(self.imBlurBlur, 0, 255,
                                         cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        self.imEdges = cv2.Canny(self.imBinary, 16, 255)

    def __isIntersection(self, imBinary):
        # stdGG = np.std(imGG)
        # print(f'std\t{stdGG:0f}')

        far_count = len(np.argwhere(imBinary[-10:])[:, 1])
        far_count_gain = far_count - self.far_count_predicted
        print(f'far count\t{far_count}\tgain\t{far_count_gain:0f}')
        if self.far_count_predicted > FAR_COUNT_GAIN_PREDICT_MIN:
            if FAR_COUNT_GAIN_MIN < far_count_gain and far_count_gain < FAR_COUNT_GAIN_MAX:
                return True
        self.far_count_predicted *= 3
        self.far_count_predicted += far_count
        self.far_count_predicted //= 4

        self.far_count_predicted = max(
            self.far_count_predicted, FAR_COUNT_GAIN_PREDICT_MIN)

        return False

    def __negativeControl(self, imEdge):
        near_sight = 10
        edges_near = np.argwhere(imEdge[0:near_sight])[:, 1]
        while len(edges_near) == 0 and near_sight < CROP_BOTTOM:
            near_sight += 10
            edges_near = np.argwhere(imEdge[0:near_sight])[:, 1]
        if len(edges_near) > 0:
            pos = np.mean(edges_near)
            diff = pos - IDEAL_POS
            print(f'\t\t\t\t\tdiff\t{diff:0f}')
            next_duty_cycle = getDutyCycle(diff)
            self.pwm.ChangeDutyCycle(next_duty_cycle)
        else:
            print('\t\t\t\t\tdiff = N/A')

    def goAhead(self):
        print('handleFollowLine() starting')

        self.motorRun()

        self.far_count_predicted = 10 * (CROP_RIGHT - CROP_LEFT)
        while True:
            self.__captureAndFilter()
            if (self.__isIntersection(self.imBinary)):
                break
            self.__negativeControl(self.imEdges)

        self.motorStop()
        time.sleep(1)

    def goLeft(self):
        self.__go90('l')

    def goRight(self):
        self.__go90('r')

    def goHalfLeft(self):
        self.__go45('l')

    def goHalfRight(self):
        self.__go45('r')

    def __go90(self, lr=''):
        self.motorRun()
        if lr == 'l':
            self.pwm.ChangeDutyCycle(DC_LEFT)
        elif lr == 'r':
            self.pwm.ChangeDutyCycle(DC_RIGHT)
        time.sleep(TIME_TURN90)
        if lr == 'l':
            self.pwm.ChangeDutyCycle(DC_L2)
        elif lr == 'r':
            self.pwm.ChangeDutyCycle(DC_R2)

        while True:
            self.__captureAndFilter()
            varBlurBlur = np.var(self.imBlurBlur)
            print(f'var\t{varBlurBlur:0f}')
            if varBlurBlur > varBlurBlur_THRESHOLD:
                break

        self.motorStop()
        time.sleep(1)

    def __go45(self, lr=''):
        self.pwm.ChangeDutyCycle(DC_CENTER)
        self.motorRun()
        time.sleep(TIME_GO45)
        if lr == 'l':
            self.pwm.ChangeDutyCycle(DC_LEFT)
        elif lr == 'r':
            self.pwm.ChangeDutyCycle(DC_RIGHT)
        time.sleep(TIME_TURN45)
        if lr == 'l':
            self.pwm.ChangeDutyCycle(DC_L2)
        elif lr == 'r':
            self.pwm.ChangeDutyCycle(DC_R2)

        while True:
            self.__captureAndFilter()
            varBlurBlur = np.var(self.imBlurBlur)
            print(f'var\t{varBlurBlur:0f}')
            if varBlurBlur > varBlurBlur_THRESHOLD:
                break

        self.motorStop()
        time.sleep(1)
