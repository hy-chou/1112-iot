import time
from os import listdir
import cv2
import numpy as np

CROP_TOP = 0  # >= 0
CROP_BOTTOM = 160  # <= 480
CROP_LEFT = 0  # >= 0
CROP_RIGHT = 640 - CROP_LEFT

# DIR = 'im-on-edge'
DIR = 'im-at-node'

files = sorted(listdir(DIR))

for file in files:
    # if file != 'im-12-south10.jpeg':
    #     continue

    print(file)

    im = cv2.imread(f'./{DIR}/{file}')
    im = cv2.rotate(im, cv2.ROTATE_180)
    im = im[CROP_TOP:CROP_BOTTOM, CROP_LEFT:CROP_RIGHT]
    im = cv2.rotate(im, cv2.ROTATE_180)
    for _ in range(3):
        im = cv2.GaussianBlur(im, (99, 99), 0)
    im = cv2.cvtColor(im, cv2.COLOR_RGB2HSV)[:, :, 1]
    _, im = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite('im_test.jpeg', im)

    time.sleep(0.1)

    # im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    # cv2.imwrite('im_gray.jpeg', im)

    # for _ in range(3):
    #     im = cv2.GaussianBlur(im, (31, 31), 0)
    # cv2.imwrite('im_blur.jpeg', im)

    # ret, im = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # print(ret)
    # cv2.imwrite('im_binary.jpeg', im)

    # im = cv2.Canny(im, 16, 255)
    # cv2.imwrite('im_canny.jpeg', im)
