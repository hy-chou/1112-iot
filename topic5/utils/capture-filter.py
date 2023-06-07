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

imG = cv2.GaussianBlur(im, (31, 31), 5)
imS = cv2.cvtColor(imG, cv2.COLOR_RGB2HSV)[:, :, 1]
imGG = cv2.GaussianBlur(imS, (31, 31), 5)
thresh, imBinary = cv2.threshold(
    imGG, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
imEdge = cv2.Canny(imBinary, 16, 255)

cv2.imwrite('imEdge.jpeg', imEdge)
