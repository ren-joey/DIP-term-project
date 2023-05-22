import numpy as np
import cv2
from utils import \
                text_to_img, \
                generate_random_by_secret_img, \
                get_da, \
                inverter, \
                norm, \
                vac1, \
                vac2, \
                get_img_resize
from plotter import img_plotter


size = (64, 64)
windows_size = 8
font_size = 30
SI = text_to_img("A", size, font_size)
RP1, RP2 = generate_random_by_secret_img(SI)
SP1, SP2 = vac1(RP1, RP2, size=windows_size)
TA1 = vac2(SP1, size=windows_size)
TA2 = vac2(SP2, size=windows_size)
img1 = get_img_resize('./img1.png', size)
img2 = get_img_resize('./img2.png', size)
for y in range(size[0]):
    for x in range(size[1]):
        if img1[y][x] > TA1[y][x]:
            img1[y][x] = 255
        else:
            img1[y][x] = 0

        if img2[y][x] > TA2[y][x]:
            img2[y][x] = 255
        else:
            img2[y][x] = 0
cv2.imwrite('./X1.png', img1)
cv2.imwrite('./X2.png', img2)
