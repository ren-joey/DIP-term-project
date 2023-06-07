import numpy as np
import cv2
import math
import random
from numba import njit
import sys
from time import process_time 

def random_set(List):
    List2 = []
    size = np.size(List) / 2
    for i in range(int(size/2)):
        random_num = random.randint(0, size-1)
        List2.append(List[random_num])
        del List[random_num]
        size -= 1

    return List2

def getRP(secret_img, rp1, rp2) :
    a = secret_img.shape[0]
    b = secret_img.shape[1]

    B = []
    W = []
    for i in range(a):
        for j in range(b):
            if secret_img[i][j] < 128:
                B.append((i,j))
            else:
                W.append((i,j))           
    #print(B,W)           
    B2 = random_set(B)
    W2 = random_set(W)

    for (i,j) in B:
        rp1[i][j] = 0
        rp2[i][j] = 1
    for (i,j) in B2:
        rp1[i][j] = 1
        rp2[i][j] = 0
    for (i,j) in W:
        rp1[i][j] = 0
        rp2[i][j] = 0
    for (i,j) in W2:
        rp1[i][j] = 1
        rp2[i][j] = 1
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
            if RP[x][y] == 1: ##white
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
    #print("Finish at", count)
    #print(np.max(DA), np.min(DA)) 
    return (RP1, RP2)
@njit()
def VAC2(noise):
    ones = 0
    DA = np.zeros((noise.shape[0], noise.shape[1]))
    TA = np.zeros((noise.shape[0], noise.shape[1]))
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
        TA[DA_ARGB[0]][DA_ARGB[1]] = rank
        B.remove((DA_ARGB[0], DA_ARGB[1]))
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
        TA[DA_ARGW[0]][DA_ARGW[1]] = rank
        W.remove((DA_ARGW[0], DA_ARGW[1]))
        updateDA(noise, DA, DA_ARGW[0], DA_ARGW[1], point_list2, Exp2)
        rank += 1
        
    TA = 255*(TA+0.5)/(noise.shape[0]*noise.shape[1])
    return TA

def filtering(img, Filter):
    res = np.zeros((img.shape[0], img.shape[1]))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            fi = i % Filter.shape[0]
            fj = j % Filter.shape[1]
            if img[i][j] > Filter[fi][fj]:
                res[i][j] = 255
            else:
                res[i][j] = 0
    return res
    
print("Step 0")
secret_image_name = sys.argv[1]
secret_img = cv2.imread(secret_image_name, cv2.IMREAD_GRAYSCALE)
RP1 = np.zeros(secret_img.shape, dtype=np.uint8)
RP2 = np.zeros(secret_img.shape, dtype=np.uint8)
getRP(secret_img, RP1, RP2) 
#cv2.imwrite('RP1.png', RP1*255)
#cv2.imwrite('RP2.png', RP2*255)

print("Step 1")
point_list = []
R = 15
for x in range(-R, R+1):
    for y in range(-R, R+1):
        if x**2+y**2 <= R**2:
            point_list.append((x,y))
point_list2 = np.array(point_list)

Exp = []
for i in range(0, R**2+1):
    Exp.append(np.exp(-i/4.5))
Exp2 = np.array(Exp)

(SP1, SP2) = VAC1(RP1, RP2, secret_img)
#cv2.imwrite("SP1.png", SP1*255)
#cv2.imwrite("SP2.png", SP2*255)

print("Step 2")
TA1 = VAC2(SP1)
TA2 = VAC2(SP2)
#cv2.imwrite("TA1.png", TA1)
#cv2.imwrite("TA2.png", TA2)

print("Step 3")
image1_name = sys.argv[2]
img1 = cv2.imread(image1_name, cv2.IMREAD_GRAYSCALE)
image2_name = sys.argv[3]
img2 = cv2.imread(image2_name, cv2.IMREAD_GRAYSCALE)
X1 = filtering(img1, TA1)
X2 = filtering(img2, TA2)
cv2.imwrite("X1.png", X1)
cv2.imwrite("X2.png", X2)
