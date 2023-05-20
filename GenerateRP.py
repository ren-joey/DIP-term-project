import cv2
import numpy as np
import random
import sys

def random_01_generator():
    random_num = random.random()
    res = round(random_num)
    return res

secret_image_name = sys.argv[1]

secret_img = cv2.imread(secret_image_name, cv2.IMREAD_GRAYSCALE)

rp1 = np.zeros(secret_img.shape, dtype=np.uint8)
rp2 = np.zeros(secret_img.shape, dtype=np.uint8)

a = secret_img.shape[0]
b = secret_img.shape[1]

for i in range(a):
    for j in range(b):
        num = random_01_generator()
        if (secret_img[i][j] >= 128):   # Seen as "W (White pixel)"
            if (num == 1):
                rp1[i][j] = 255
                rp2[i][j] = 255
            else:
                rp1[i][j] = 0
                rp2[i][j] = 0
        else:   # Seen as "B (Black pixel)"
            if (num == 1):
                rp1[i][j] = 255
                rp2[i][j] = 0
            else:
                rp1[i][j] = 0
                rp2[i][j] = 255

cv2.imwrite('RP1.png', rp1)
cv2.imwrite('RP2.png', rp2)

