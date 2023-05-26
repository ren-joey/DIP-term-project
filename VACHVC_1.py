import numpy as np
import cv2
import math
import random
from numba import njit
import sys
from time import process_time 

@njit()   
def getDA(noise, x, y, point_list2, Exp):
    res = 0
    M = noise.shape[1]
    N = noise.shape[0]
    for [p, q] in point_list2:
        p2 = (x-p)%N
        q2 = (y-q)%M
        if noise[p2][q2] == 0:
            res += Exp[p**2+q**2]
    return res
@njit()
def updateDA(noise, DA, x, y, point_list2, Exp):
    M = noise.shape[1]
    N = noise.shape[0]
    for [p, q] in point_list2:
        p2 = (x-p)%N
        q2 = (y-q)%M
        value = Exp[p**2+q**2]
        if noise[x][y] == 0:
            DA[p2][q2] += value
        else:
            DA[p2][q2] -= value      
    return
@njit()
def VAC1(RP1, RP2, SEC):
    DA1 = np.zeros((RP1.shape[0], RP1.shape[1]))
    for x in range(DA1.shape[0]):
        for y in range(DA1.shape[1]):
            DA1[x][y] = getDA(RP1, x, y, point_list2, Exp2)
    DA2 = np.zeros((RP2.shape[0], RP2.shape[1]))        
    for x in range(DA1.shape[0]):
        for y in range(DA1.shape[1]):
            DA2[x][y] = getDA(RP2, x, y, point_list2, Exp2)
     
    B = []
    W = []
    for x in range(SEC.shape[0]):
        for y in range(SEC.shape[1]):
            if SEC[x][y] == 0:
                B.append((x,y))
            else:
                W.append((x,y))     
    
    max_iter = int(SEC.shape[0]*SEC.shape[1])/4
    #max_iter = 1
    for count in range(max_iter):
        random_num = random.randint(1, 2)
        if random_num == 1:
            RP = RP1
            DA = DA1
        else:
            RP = RP2
            DA = DA2
        DA_B = -1
        DA_ARGB = [-1, -1]
        for x in range(RP.shape[0]):
            for y in range(RP.shape[1]):
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
         
        #Swap and Update
        #print(random_num, " Exchange:", DA_ARGB[0], DA_ARGB[1], " and ", DA_ARGW[0], DA_ARGW[1])
        (RP1[DA_ARGB[0]][DA_ARGB[1]], RP1[DA_ARGW[0]][DA_ARGW[1]]) = (RP1[DA_ARGW[0]][DA_ARGW[1]], RP1[DA_ARGB[0]][DA_ARGB[1]])
        (RP2[DA_ARGB[0]][DA_ARGB[1]], RP2[DA_ARGW[0]][DA_ARGW[1]]) = (RP2[DA_ARGW[0]][DA_ARGW[1]], RP2[DA_ARGB[0]][DA_ARGB[1]])
        updateDA(RP1, DA1, DA_ARGB[0], DA_ARGB[1], point_list2, Exp2)
        updateDA(RP1, DA1, DA_ARGW[0], DA_ARGW[1], point_list2, Exp2)
        updateDA(RP2, DA2, DA_ARGB[0], DA_ARGB[1], point_list2, Exp2)
        updateDA(RP2, DA2, DA_ARGW[0], DA_ARGW[1], point_list2, Exp2)
        if count%1000 == 0:
            print(count, np.max(DA1), np.min(DA1), np.max(DA2), np.min(DA2))
        if DA[DA_ARGB[0]][DA_ARGB[1]] <= np.min(DA):
            (RP1[DA_ARGB[0]][DA_ARGB[1]], RP1[DA_ARGW[0]][DA_ARGW[1]]) = (RP1[DA_ARGW[0]][DA_ARGW[1]], RP1[DA_ARGB[0]][DA_ARGB[1]])
            break
    print("Finish at", count)
    #print(np.max(DA), np.min(DA)) 
    #print(np.argmax(DA), np.argmin(DA))
    return (RP1, RP2)

#start = process_time()
RP1 = cv2.imread("RP1.png", cv2.IMREAD_GRAYSCALE)/255
RP2 = cv2.imread("RP2.png", cv2.IMREAD_GRAYSCALE)/255
SEC = cv2.imread("secret.png", cv2.IMREAD_GRAYSCALE)/255
if(RP1.shape[0] != RP2.shape[0] or RP1.shape[1] != RP2.shape[1]):
    print("RP size error!")
if(RP1.shape[0] != SEC.shape[0] or RP1.shape[1] != SEC.shape[1]):
    print("The size of SECRET must be equal to that of RPs!")
    
point_list = []
R = 5
print("r=", R)
for x in range(-R, R+1):
    for y in range(-R, R+1):
        if x**2+y**2 <= R**2:
            point_list.append((x,y))
point_list2 = np.array(point_list)

Exp = []
for i in range(0, R**2+1):
    Exp.append(np.exp(-i/4.5))
Exp2 = np.array(Exp)       

(SP1, SP2) = VAC1(RP1, RP2, SEC)
cv2.imwrite("SP1.png", SP1*255)
cv2.imwrite("SP2.png", SP2*255)
#print("Time:", process_time() - start)