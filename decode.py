import numpy as np
import cv2
import sys

def max(a, b):
    c = b
    if (a >= b):
        c = a
    return c

def merge(X1, X2):
    a = X1.shape[0]
    b = X1.shape[1]
    res = np.zeros(X1.shape, dtype=np.uint8)
    for i in range(a):
        for j in range(b):
            res[i][j] = max(X1[i][j], X2[i][j])
    return res

X1_name = sys.argv[1]
X2_name = sys.argv[2]

X1 = cv2.imread(X1_name, cv2.IMREAD_GRAYSCALE)
X2 = cv2.imread(X2_name, cv2.IMREAD_GRAYSCALE)

decode_img = merge(X1, X2)
cv2.imwrite('decode.png', decode_img)

