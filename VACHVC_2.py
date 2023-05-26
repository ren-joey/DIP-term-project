import numpy as np
import cv2
import math
from numba import njit
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
def VAC2(noise):
    ones = 0
    DA = np.zeros((noise.shape[0], noise.shape[1]))
    NDA = np.zeros((noise.shape[0], noise.shape[1]))
    for x in range(0, noise.shape[0]):
        for y in range(0, noise.shape[1]):
            DA[x][y] = getDA(noise, x, y, point_list2, Exp2)
    #Get B and W coor
    B = []
    W = []
    for x in range(noise.shape[0]):
        for y in range(noise.shape[1]):
            if noise[x][y] == 0:
                B.append((x,y))
            else:
                W.append((x,y))
    ones = len(B)
    #Phase I
    print("P1")
    rank = ones-1
    noise2 = np.copy(noise)
    DA2 = np.copy(DA)      
    while rank >= 0:
        DA_B = -1
        DA_ARGB = [-1, -1]
        for (x, y) in B:
            if DA2[x][y] > DA_B:
                DA_B = DA2[x][y]
                DA_ARGB = [x, y]
        noise2[DA_ARGB[0]][DA_ARGB[1]] = 1
        NDA[DA_ARGB[0]][DA_ARGB[1]] = rank
        B.remove((DA_ARGB[0], DA_ARGB[1]))
        if rank%1000 == 0:
            print(rank, DA_ARGB[0], DA_ARGB[1])
        updateDA(noise2, DA2, DA_ARGB[0], DA_ARGB[1], point_list2, Exp2)
        rank -= 1
        
    #Phase II
    print("P2")#P2=P3
    
    #Phase III    
    print("P3")
    rank = ones
    while rank < (noise.shape[0]*noise.shape[1]):
        DA_W = -1+2**31
        DA_ARGW = [-1, -1]
        for (x, y) in W:
            if DA[x][y] < DA_W:
                DA_W = DA[x][y]
                DA_ARGW = [x, y]
        noise[DA_ARGW[0]][DA_ARGW[1]] = 0
        NDA[DA_ARGW[0]][DA_ARGW[1]] = rank
        if (DA_ARGW[0], DA_ARGW[1]) in W:
            W.remove((DA_ARGW[0], DA_ARGW[1]))
        else:
            print(rank, B, W)
        if rank%1000 == 0:
            print(rank, DA_ARGW[0], DA_ARGW[1])
        updateDA(noise, DA, DA_ARGW[0], DA_ARGW[1], point_list2, Exp2)
        rank += 1
        
    NDA = 255*(NDA+0.5)/(noise.shape[0]*noise.shape[1])
    return NDA
    
start = process_time()
sp1 = cv2.imread("SP1.png", cv2.IMREAD_GRAYSCALE)/255
sp2 = cv2.imread("SP2.png", cv2.IMREAD_GRAYSCALE)/255

#point_list = []
R = math.ceil(math.sqrt(sp1.shape[0]**2 + sp1.shape[1]**2)/3)
if R >= 15: R = 15
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
        
ta1 = VAC2(sp1)
cv2.imwrite("TA1.png", ta1)

ta2 = VAC2(sp2)
cv2.imwrite("TA2.png", ta2)
#print("Time:", process_time() - start)