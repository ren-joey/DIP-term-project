import cv2
import numpy as np

def f(x):
    y = (191-64)/(255-0)*x + 64
    return y

img = cv2.imread('dog1.png', cv2.IMREAD_GRAYSCALE)
print(img.max(), img.min())

img2 = cv2.imread('dog2.png', cv2.IMREAD_GRAYSCALE)
print(img2.max(), img2.min())

img_out = np.zeros(img.shape, dtype=np.uint8)
img_out2 = np.zeros(img2.shape, dtype=np.uint8)

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        img_out[i][j] = f(img[i][j])
        img_out2[i][j] = f(img2[i][j])

cv2.imwrite('Dog1.png', img_out)
cv2.imwrite('Dog2.png', img_out2)

