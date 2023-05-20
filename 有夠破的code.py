import numpy as np
import cv2
import math

def findDA(noise, x, y):
    res = 0
    M = noise.shape[1]
    N = noise.shape[0]
    R = int(M/2) #size of filter, default = int(M/2)
    for p in range(-R, R+1):
        for q in range(-R, R+1):
            p2 = (N+x-p)%N
            q2 = (M+y-q)%M
            if noise[p2][q2] == 0:
                res += Exp[p**2+q**2]
    return res
    
##VAC-1
noise = cv2.imread("noise.png", cv2.IMREAD_GRAYSCALE)/255
Exp = []
for i in range(0, 100000):
    Exp.append(np.exp(-i/4.5))
    
DA = np.zeros((noise.shape[0], noise.shape[1]))
while 1:
    DA_B = -1
    DA_ARGB = [-1, -1]
    DA_W = -1+2**31
    DA_ARGW = [-1, -1]
    for x in range(0, noise.shape[0]):
        for y in range(0, noise.shape[1]):
            DA[x][y] = findDA(noise, x, y)
            if noise[x][y] == 0:
                if DA[x][y] > DA_B:
                    DA_B = DA[x][y]
                    DA_ARGB = [x, y]
            else:
                if DA[x][y] < DA_W:
                    DA_W = DA[x][y]
                    DA_ARGW = [x, y]
                
    noise[DA_ARGB[0]][DA_ARGB[1]] = 1
    if findDA(noise, DA_ARGB[0], DA_ARGB[1]) <= DA_W:
        print(DA_ARGW[0], DA_ARGW[1], "!")
        noise[DA_ARGB[0]][DA_ARGB[1]] = 0   
        break
    else:
        print(DA_ARGW[0], DA_ARGW[1])
        noise[DA_ARGW[0]][DA_ARGW[1]] = 0    
cv2.imwrite("blue_noise.png", noise*255)

