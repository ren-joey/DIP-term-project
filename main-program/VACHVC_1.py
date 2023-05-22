import numpy as np
import cv2
import math
import threading
import random    

def findDA(noise, x, y):
    res = 0
    M = noise.shape[1]
    N = noise.shape[0]
    R = 5 #size of filter, default = int(M/2)
    for p in range(-R, R+1):
        for q in range(-R, R+1):
            p2 = (x-p)%N
            q2 = (y-q)%M
            if noise[p2][q2] == 0:
                res += Exp[p**2+q**2]
    return res

def updateDA(noise, DA, x, y):
    M = noise.shape[1]
    N = noise.shape[0]
    R = 5 #size of filter, default = int(M/2)
    if noise[x][y] == 0: #black point
        for p in range(-R, R+1):
            for q in range(-R, R+1):
                p2 = (x-p)%N
                q2 = (y-q)%M
                DA[p2][q2] += Exp[p**2+q**2]
    else:                #white point
        for p in range(-R, R+1):
            for q in range(-R, R+1):
                p2 = (x-p)%N
                q2 = (y-q)%M
                DA[p2][q2] -= Exp[p**2+q**2]
    return

def VAC1(RP1, RP2, SEC):
    DA1 = np.zeros((RP1.shape[0], RP1.shape[1]))
    DA2 = np.zeros((RP2.shape[0], RP2.shape[1]))
    for x in range(0, DA1.shape[0]):
        for y in range(0, DA1.shape[1]):
            DA1[x][y] = findDA(RP1, x, y)
            DA2[x][y] = findDA(RP2, x, y)
            
    B = []
    W = []        
    for x in range(0, DA1.shape[0]):
        for y in range(0, DA1.shape[1]):
            if SEC[x][y] == 0:
                B.append((x,y))
            else:
                W.append((x,y))     

    for count in range(0, int(SEC.shape[0]*SEC.shape[1]/10)): ##A large number
        if random.randint(1, 2) == 1:
            RP = RP1
            DA = DA1
        else:
            RP = RP2
            DA = DA2
        DA_B = -1
        DA_ARGB = [-1, -1]
        for x in range(0, RP.shape[0]):
            for y in range(0, RP.shape[1]):
                if RP[x][y] == 0: ##black
                    if DA[x][y] > DA_B:
                        DA_B = DA[x][y]
                        DA_ARGB = [x, y]
        
        if SEC[DA_ARGB[0]][DA_ARGB[1]] == 0:
            region = B
        else:
            region = W
        DA_W = -1+2**31
        DA_ARGW = [-1, -1]
        for (x,y) in region:
            if RP[x][y] == 1:
                if DA[x][y] < DA_W:
                    DA_W = DA[x][y]
                    DA_ARGW = [x, y]
                    
        #swap        
        (RP1[DA_ARGB[0]][DA_ARGB[1]], RP1[DA_ARGW[0]][DA_ARGW[1]]) = (RP1[DA_ARGW[0]][DA_ARGW[1]], RP1[DA_ARGB[0]][DA_ARGB[1]])
        (RP2[DA_ARGB[0]][DA_ARGB[1]], RP2[DA_ARGW[0]][DA_ARGW[1]]) = (RP2[DA_ARGW[0]][DA_ARGW[1]], RP2[DA_ARGB[0]][DA_ARGB[1]])
        if DA[DA_ARGB[0]][DA_ARGB[1]]-1 <= DA_W:
            print(DA_ARGW[0], DA_ARGW[1], "!")
            break
        else:
            print(DA_ARGB[0], DA_ARGB[1], DA_ARGW[0], DA_ARGW[1])
            updateDA(RP1, DA1, DA_ARGB[0], DA_ARGB[1])
            updateDA(RP1, DA1, DA_ARGW[0], DA_ARGW[1])
            updateDA(RP2, DA2, DA_ARGB[0], DA_ARGB[1])
            updateDA(RP2, DA2, DA_ARGW[0], DA_ARGW[1])            
    return (RP1, RP2)

Exp = []
for i in range(0, 100000):
    Exp.append(np.exp(-i/4.5)) #approximately equal to 0.8^i
        
RP1 = cv2.imread("RP1.png", cv2.IMREAD_GRAYSCALE)/255
RP2 = cv2.imread("RP2.png", cv2.IMREAD_GRAYSCALE)/255
SEC = cv2.imread("secret.png", cv2.IMREAD_GRAYSCALE)/255
(SP1, SP2) = VAC1(RP1, RP2, SEC)
cv2.imwrite("SP1.png", SP1*255)
cv2.imwrite("SP2.png", SP2*255)
#cv2.imwrite("SP3.png", RP1*255)
#cv2.imwrite("SP4.png", RP2*255)