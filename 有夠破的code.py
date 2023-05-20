import numpy as np
import cv2
import math
import threading

def fillDA(DA, x):
    for y in range(0, noise.shape[1]):
            DA[x][y] = findDA(noise, x, y)
    return
    
def findDA(noise, x, y):
    res = 0
    M = noise.shape[1]
    N = noise.shape[0]
    R = int(M/2) #size of filter, default = int(M/2)
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
    R = int(M/2)
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

def VAC1(noise):
    DA = np.zeros((noise.shape[0], noise.shape[1]))
    for x in range(0, noise.shape[0]):
        print(x)
        for y in range(0, noise.shape[1]):
            DA[x][y] = findDA(noise, x, y)
        
    for count in range(0, noise.shape[0]*noise.shape[1]):
        DA_B = -1
        DA_ARGB = [-1, -1]
        DA_W = -1+2**31
        DA_ARGW = [-1, -1]
        for x in range(0, noise.shape[0]):
            for y in range(0, noise.shape[1]):
                if noise[x][y] == 0:
                    if DA[x][y] > DA_B:
                        DA_B = DA[x][y]
                        DA_ARGB = [x, y]
                else:
                    if DA[x][y] < DA_W:
                        DA_W = DA[x][y]
                        DA_ARGW = [x, y]
                
        noise[DA_ARGB[0]][DA_ARGB[1]] = 1
        if DA[DA_ARGB[0]][DA_ARGB[1]]-1 <= DA_W:
            print(DA_ARGW[0], DA_ARGW[1], "!")
            noise[DA_ARGB[0]][DA_ARGB[1]] = 0   
            break
        else:
            print(DA_ARGB[0], DA_ARGB[1], DA_ARGW[0], DA_ARGW[1])
            noise[DA_ARGW[0]][DA_ARGW[1]] = 0
            updateDA(noise, DA, DA_ARGB[0], DA_ARGB[1])
            updateDA(noise, DA, DA_ARGW[0], DA_ARGW[1])   
    return noise 

def VAC2(noise):
    ones = 0
    DA = np.zeros((noise.shape[0], noise.shape[1]))
    NDA = np.zeros((noise.shape[0], noise.shape[1]))
    for x in range(0, noise.shape[0]):
        print(x)
        for y in range(0, noise.shape[1]):
            DA[x][y] = findDA(noise, x, y)
            if  noise[x][y] == 0:
                ones += 1
    rank = ones-1
    
    #Phase I
    print("P1")
    noise2 = np.copy(noise)
            
    while rank >= 0:
        DA2 = np.copy(DA)
        DA_B = -1
        DA_ARGB = [-1, -1]
        for x in range(0, noise2.shape[0]):
            for y in range(0, noise2.shape[1]):
                if noise2[x][y] == 0:
                    if DA2[x][y] > DA_B:
                        DA_B = DA2[x][y]
                        DA_ARGB = [x, y]
        noise2[DA_ARGB[0]][DA_ARGB[1]] = 1
        NDA[DA_ARGB[0]][DA_ARGB[1]] = rank
        print(rank, DA_ARGB[0], DA_ARGB[1])
        updateDA(noise2, DA2, DA_ARGB[0], DA_ARGB[1])
        rank -= 1
    #Phase II
    print("P2")
    rank = ones
    
    while rank < (noise.shape[0]*noise.shape[1]/2):
        DA_W = -1+2**31
        DA_ARGW = [-1, -1]
        for x in range(0, noise.shape[0]):
            for y in range(0, noise.shape[1]):
                if noise[x][y] == 1:
                    if DA[x][y] < DA_W:
                        DA_W = DA[x][y]
                        DA_ARGW = [x, y]
        noise[DA_ARGW[0]][DA_ARGW[1]] = 0
        NDA[DA_ARGW[0]][DA_ARGW[1]] = rank
        print(rank, DA_ARGW[0], DA_ARGW[1])
        updateDA(noise, DA, DA_ARGW[0], DA_ARGW[1])
        rank += 1
        
    #Phase III    
    print("P3")
    while rank < (noise.shape[0]*noise.shape[1]):
        DA_W = -1+2**31
        DA_ARGW = [-1, -1]
        for x in range(0, noise.shape[0]):
            for y in range(0, noise.shape[1]):
                if noise[x][y] == 1:
                    if DA[x][y] < DA_W:
                        DA_W = DA[x][y]
                        DA_ARGW = [x, y]
        noise[DA_ARGW[0]][DA_ARGW[1]] = 0
        NDA[DA_ARGW[0]][DA_ARGW[1]] = rank
        print(rank, DA_ARGW[0], DA_ARGW[1])
        updateDA(noise, DA, DA_ARGW[0], DA_ARGW[1])
        rank += 1
    NDA = 255*(NDA+0.5)/rank
    cv2.imwrite("DA_0.png", NDA)
    return NDA.astype(int)
        
Exp = []
for i in range(0, 100000):
    Exp.append(np.exp(-i/4.5))
        
noise = cv2.imread("noise.png", cv2.IMREAD_GRAYSCALE)/255
b_noise = VAC1(noise)
cv2.imwrite("blue_noise.png", b_noise*255)
b_noise = cv2.imread("blue_noise.png", cv2.IMREAD_GRAYSCALE)/255
NDA = VAC2(b_noise)
cv2.imwrite("DA.png", NDA)

