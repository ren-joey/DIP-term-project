from random import randint

import cv2
import numpy as np
from text_to_img import text_to_img
from plotter import img_plotter

def generate_random_by_secret_img(SI):
    RP1, RP2 = np.zeros(SI.shape, dtype=np.uint8), \
                np.zeros(SI.shape, dtype=np.uint8)
    h = SI.shape[0]
    w = SI.shape[1]

    for y in range(h):
        for x in range(w):
            seed = randint(0, 1)
            if SI[y][x] == 0:
                if seed == 0:
                    RP1[y][x] = 0
                    RP2[y][x] = 255
                else:
                    RP1[y][x] = 255
                    RP2[y][x] = 0
            else:
                if seed == 0:
                    RP1[y][x] = 0
                    RP2[y][x] = 0
                else:
                    RP1[y][x] = 255
                    RP2[y][x] = 255
    return RP1, RP2

SI = text_to_img("SECRET", (256, 256), 36)
RP1, RP2 = generate_random_by_secret_img(SI)


