import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt

def text_to_img(text, imgsize, fontsize=24):
    # plt.text(0, imgsize[1]//2, text, fontsize=fontsize)
    # plt.axis('off')
    # plt.savefig('msg.png')

    font = ImageFont.truetype('./font.ttf', size=fontsize)
    img = Image.new(mode="L", size=imgsize, color="white")
    draw = ImageDraw.Draw(img)
    draw.text((0, (imgsize[1] - fontsize) // 2), text, font=font)
    img.save('./msg.png')
    msg = cv2.imread('./msg.png', cv2.IMREAD_GRAYSCALE)
    return msg

arr = text_to_img("Sample text", (256, 256), 36)
cv2.imwrite('./result1.png', arr)

print(arr)