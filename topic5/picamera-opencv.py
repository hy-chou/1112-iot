import cv2
import numpy as np
from picamera2 import Picamera2

CROP_TOP = 0  # >= 0
CROP_BOTTOM = 160  # <= 480
CROP_LEFT = 0  # >= 0
CROP_RIGHT = 640 - CROP_LEFT


picam2 = Picamera2()
picam2.start()


im = picam2.capture_array()
im = im[CROP_TOP:CROP_BOTTOM, CROP_LEFT:CROP_RIGHT]
im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
im = cv2.rotate(im, cv2.ROTATE_180)

cv2.imwrite('im.jpeg', im)

im = cv2.GaussianBlur(im, (31, 31), 5)
im = cv2.cvtColor(im, cv2.COLOR_RGB2HSV)[:, :, 1]

cv2.imwrite('im_BS.jpeg', im)

im = cv2.GaussianBlur(im, (31, 31), 5)
thresh, im = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

cv2.imwrite('im_BSBT.jpeg', im)

im = cv2.Canny(im, 16, 255)

cv2.imwrite('im_BSBTC.jpeg', im)
