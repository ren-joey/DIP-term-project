import math
from random import randint
import numpy as np
import cv2
from PIL import ImageFont, Image, ImageDraw
from plotter import img_plotter
from numpy import unravel_index

inverter = np.vectorize(lambda x: 255 if x == 0 else 0)
norm = np.vectorize(lambda x: 1 if x == 255 else 0)


def text_to_img (text, imgsize, fontsize=24):
    """
    將輸入的文字轉成黑白的圖片，可指定圖片大小
    :return msg: np.array(), dtype=uint8
    :example
    text_to_img("SECRET", (256, 256), 36)
    """
    font = ImageFont.truetype('./font.ttf', size=fontsize)
    img = Image.new(mode="L", size=imgsize, color="white")
    draw = ImageDraw.Draw(img)
    draw.text((0, (imgsize[1] - fontsize) // 2), text, font=font)
    img.show()
    img.save('./msg.png')
    msg = cv2.imread('./msg.png', cv2.IMREAD_GRAYSCALE)
    return msg


def generate_random_by_secret_img(si):
    """
    依照 Secret Image 產生對應的兩張 RPs
    :param si: Secret image -> np.array
    :return: rp1, rp2
    """
    rp1, rp2 = np.zeros(si.shape, dtype=np.uint8), \
                np.zeros(si.shape, dtype=np.uint8)
    h = si.shape[0]
    w = si.shape[1]

    for y in range(h):
        for x in range(w):
            seed = randint(0, 1)
            if si[y][x] == 0:
                if seed == 0:
                    rp1[y][x] = 0
                    rp2[y][x] = 255
                else:
                    rp1[y][x] = 255
                    rp2[y][x] = 0
            else:
                if seed == 0:
                    rp1[y][x] = 0
                    rp2[y][x] = 0
                else:
                    rp1[y][x] = 255
                    rp2[y][x] = 255

    img_plotter(
        [rp1, rp2],
        ['RP1', 'RP2']
    )
    cv2.imwrite('./RP1.png', rp1)
    cv2.imwrite('./RP2.png', rp2)

    return rp1, rp2


def get_da(img, sigma=1.5, target=255, m=None):
    """
    依照傳入的 image(BP) 來決定對應的 DA matrix
    :param img: BP image
    :param size: window size，預設為 img 的高
    :param sigma: 預設為 1.5
    :param target: 目標 grayscale, 255=cluster, 0=void
    :return:
    """
    da = np.zeros(img.shape, dtype=float)
    if m is None:
        m = img.shape[0]
    iter_range = m // 2
    divider = 2 * sigma**2

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            sum = 0

            for q in range(-iter_range, iter_range+1):
                for p in range(-iter_range, iter_range+1):
                    q_ = y-q
                    p_ = x-p

                    try:
                        if img[q_][p_] != target:
                            continue

                        r = p**2 + q**2
                        weighting = pow(math.e, -(r / divider))
                        sum += weighting

                        # print(x, y, p, q, p_, q_, r, weighting)
                    except IndexError:
                        continue
            da[y][x] = sum
    return da


def vac1(rp1, rp2, size=16):
    sp1 = np.array(rp1)
    sp2 = np.array(rp2)

    for y in range(0, sp1.shape[0], size):
        for x in range(0, sp1.shape[1], size):
            while True:
                window1 = sp1[y:y + size, x:x + size]
                window2 = sp2[y:y + size, x:x + size]
                # print('==default==')
                # print(window1)

                nw = norm(window1)
                da = get_da(window1)
                da_remove_zeros = da * nw
                max_pos = unravel_index(da_remove_zeros.argmax(), da.shape)
                window1[max_pos[0]][max_pos[1]] = 0
                window2[max_pos[0]][max_pos[1]] = 0
                # print('==remove==')
                # print(max_pos)
                # print(window1)
                # print(da)

                da = get_da(window1, target=0)
                inw = norm(inverter(window1))
                da_remove_255 = da * inw
                min_pos = unravel_index(da_remove_255.argmax(), da.shape)

                if max_pos != min_pos:
                    window1[min_pos[0]][min_pos[1]] = 255
                    window2[min_pos[0]][min_pos[1]] = 255

                    # print('==add==')
                    # print(min_pos)
                    # print(window1)
                    # print(da)
                    # print(inw)
                else:
                    window1[max_pos[0]][max_pos[1]] = 255
                    window2[max_pos[0]][max_pos[1]] = 255

                    # print('==restore==')
                    # print(max_pos)
                    # print(window1)
                    break

    img_plotter(
        [sp1, sp2],
        ['SP1', 'SP2']
    )
    cv2.imwrite('./SP1.png', sp1)
    cv2.imwrite('./SP2.png', sp2)

    return sp1, sp2


def da_norm(da):
    da = np.array(da)
    m = da.shape[1]
    n = da.shape[0]
    norm255 = np.vectorize(lambda x: (x/(m*n))*255, otypes=[np.uint8])
    return norm255(da)


def vac2(sp, size=16):
    sp = np.array(sp)
    da = np.zeros(sp.shape)
    m = sp.shape[1]
    n = sp.shape[0]
    ones = np.array([1 if x == 255 else 0 for x in sp.flatten()]).sum() - 1

    print('# PHASE I')
    rank = ones - 1
    sp2 = np.array(sp)
    prev = 0
    while rank >= 0:
        da_ = get_da(sp2, m=size)
        nw = norm(sp2)
        da_remove_zeros = da_ * nw
        max_pos = unravel_index(da_remove_zeros.argmax(), da.shape)
        sp2[max_pos[0]][max_pos[1]] = 0
        da[max_pos[0]][max_pos[1]] = rank
        rank -= 1

        ones = np.array([1 if x != 0 else 0 for x in da.flatten()]).sum()
        if prev == ones:
            print(nw[max_pos[0]][max_pos[1]])
            print(sp2)
            print(max_pos)
        prev = ones

    print('# PHASE II')
    rank = ones
    while rank < m*n/2:
        da_ = get_da(sp, target=0, m=size)
        inw = norm(inverter(sp))
        da_remove_255 = da_ * inw
        min_pos = unravel_index(da_remove_255.argmax(), da.shape)
        sp[min_pos[0]][min_pos[1]] = 255
        da[min_pos[0]][min_pos[1]] = rank
        rank += 1

        ones = np.array([1 if x != 0 else 0 for x in da.flatten()]).sum()
        if prev == ones:
            print(nw[max_pos[0]][max_pos[1]])
            print(sp)
            print(max_pos)
        prev = ones

    print('# PHASE III')
    # isp = inverter(sp)
    while rank < m*n:
        da_ = get_da(sp, target=0, m=size)
        inw = norm(inverter(sp))
        da_remove_255 = da_ * inw
        min_pos = unravel_index(da_remove_255.argmax(), da.shape)
        sp[min_pos[0]][min_pos[1]] = 255
        da[min_pos[0]][min_pos[1]] = rank
        rank += 1

        ones = np.array([1 if x != 0 else 0 for x in da.flatten()]).sum()
        if prev == ones:
            print(inw[max_pos[0]][max_pos[1]])
            print(sp)
            print(min_pos)
        prev = ones

    normed_da = da_norm(da)
    print(da)
    print(normed_da)

    return normed_da


def get_img_resize(path, size, color=cv2.IMREAD_GRAYSCALE):
    img = cv2.imread(path, color)
    img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    return np.array(img)

