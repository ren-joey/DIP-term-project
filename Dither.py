import numpy as np
import cv2
import math
import sys

filename = sys.argv[1]
filtername = sys.argv[2]
resultname = sys.argv[3]
img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
Filter = cv2.imread(filtername, cv2.IMREAD_GRAYSCALE)
res = np.zeros((img.shape[0], img.shape[1]))
for i in range(0, img.shape[0]):
    for j in range(0, img.shape[1]):
        fi = i % img.shape[0]
        fj = j % img.shape[1]
        if img[i][j] > Filter[fi][fj]:
            res[i][j] = 255
        else:
            res[i][j] = 0
cv2.imwrite(resultname, res)