import cv2
from picamera2 import Picamera2

CROP_HEIGHT = 40

picam2 = Picamera2()
picam2.start()

im = picam2.capture_array()

crop_im = im[:CROP_HEIGHT]

gray = cv2.cvtColor(crop_im, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
ret, thresh = cv2.threshold(
    blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

cv2.imwrite('test_ori.jpeg', im)
cv2.imwrite('test_thr.jpeg', thresh)
