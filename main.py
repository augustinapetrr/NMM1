import numpy as np
import matplotlib.pyplot as mpl
import re

maxIterations = 50
epsilon = 10**-8
myInfinity = 1000000

# Variables for color diagram

reMin, reMax, imMin, imMax = -2, 2, -2, 2
resolution = 400
z0Grid = []
maxDiffGrid = np.zeros((resolution, resolution))

# -------------Getting input of r-------------

def parseComplexString (complexStr):
    complexStr = ((complexStr.replace('(', '')).replace(')', '')).split(", ")
    return float(complexStr[0]), float(complexStr[1]);

tempR = 0;
while tempR == 0:
    print('Enter complex parameter r: ')
    tempR = input()
    if re.search("^\(\d+, \d+\)$", tempR) or re.search("^\(\d+\.\d+, \d+\.\d+\)$", tempR) or re.search("^\(\d+\.\d+, \d+\)$", tempR) or re.search("^\(\d+, \d+\.\d+\)$", tempR):
        r1, r2 = parseComplexString(tempR)
        r = complex(r1, r2)
    else:
        tempR = 0
        print("Format: (X, Y) where X and Y are numbers!")

# -------------Calculating max(k = 0, 1, ..., 50)|wk-zk|-------------

def getMaxDiff(z0):
    z = z0
    w = z0 + epsilon
    maxDiff = 0

    for _ in range(maxIterations + 1):
        diff = abs(w - z)

        if diff > myInfinity:
            break
        elif diff > maxDiff:
            maxDiff = diff

        z = z**2 + r
        w = w**2 + r
    
    return maxDiff

# -------------Preparing for the color diagram-------------

reVal = np.linspace(reMin, reMax, resolution)
imVal = np.linspace(imMin, imMax, resolution)

# Creating z0 grid

for i in imVal:
    row = []
    for r in reVal:
        row.append(complex(r, i))
    z0Grid.append(row)
        
z0Grid = np.array(z0Grid)

# Calculating max difference for each z0

for i in range(resolution):
    for j in range(resolution):
        z0 = z0Grid[i, j]
        maxDiffGrid[i, j] = getMaxDiff(z0)

# -------------Rendering the color diagram-------------

mpl.figure(figsize=(8, 8))
mpl.imshow(maxDiffGrid, extent=[reMin, reMax, imMin, imMax], cmap='gist_gray_r', origin='lower')
mpl.colorbar(label=r'$\max |w_k - z_k|$')
mpl.xlabel(r'Re$(z_0)$')
mpl.ylabel(r'Im$(z_0)$')
mpl.show()