import cv2
import numpy as np
from picamera2 import Picamera2

CROP_TOP = 0
CROP_BOTTOM = 80
CROP_LEFT = 0
CROP_RIGHT = 640 - CROP_LEFT


picam2 = Picamera2()
picam2.start()


im = picam2.capture_array()
im = im[CROP_TOP:CROP_BOTTOM, CROP_LEFT:CROP_RIGHT]
# im = cv2.rotate(im, cv2.ROTATE_180)
cv2.imwrite('im_bgr.jpeg', im)

im_b, im_g, im_r = im[:, :, 0], im[:, :, 1], im[:, :, 2]

im_b = cv2.GaussianBlur(im_b, (5, 5), 0)
im_g = cv2.GaussianBlur(im_g, (5, 5), 0)
im_r = cv2.GaussianBlur(im_r, (5, 5), 0)
_, im_b = cv2.threshold(im_b, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
_, im_g = cv2.threshold(im_g, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
_, im_r = cv2.threshold(im_r, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

im = np.logical_and(im_b, im_g)
im = np.logical_and(im, im_r) * 255
cv2.imwrite('im_gray.jpeg', im)

print(im.shape)
