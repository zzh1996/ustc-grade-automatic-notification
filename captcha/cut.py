#!/usr/bin/env python
import numpy as np
import cv2
import sys

def cut(filename):
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    final = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
    cells = np.hsplit(final, 4)
    for i in range(4):
        cv2.imwrite(filename.split('.')[0] + str(i) + '.jpg', cells[i])

if __name__ == '__main__':
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        cut(filename)
