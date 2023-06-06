import cv2
import numpy as np
from picamera2 import Picamera2

CROP_TOP = 0  # >= 0
CROP_BOTTOM = 80  # <= 480
CROP_LEFT = 0  # >= 0
CROP_RIGHT = 640 - CROP_LEFT


picam2 = Picamera2()
picam2.start()


im = picam2.capture_array()
im = im[CROP_TOP:CROP_BOTTOM, CROP_LEFT:CROP_RIGHT]
im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
im = cv2.rotate(im, cv2.ROTATE_180)
cv2.imwrite('im.jpeg', im)

im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
im = cv2.GaussianBlur(im, (49, 49), 0)
_, im = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imwrite('im_binary.jpeg', im)

im = cv2.Canny(im, 16, 255)
cv2.imwrite('im_canny.jpeg', im)
