#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from skimage import feature

def findEdges(im):

    edges = feature.canny(im)
    return edges

def genBoundaryPoints(im, thin=1):
    
    Nx, Ny = im.shape

    axX = np.arange(Nx)
    axY = np.arange(Ny)

    X, Y = np.meshgrid(axX, axY)
    """
    print X.shape
    print Y.shape
    edges = findEdges(im)
    X = X[edges]
    Y = Y[edges]

    print X.shape
    print Y.shape

    XY = zip(X, Y)

    plt.plot(X, Y)
    plt.show()

    return XY
    """

    fig, ax = plt.subplots()
    C = ax.contour(X, Y, im, levels=[0.5])

    segs = C.allsegs[0]

    points = []

    for seg in segs:
        print seg.shape
        if seg.shape[0] % thin == 0:
            #line = np.zeros((seg.shape[0]/thin-1, seg.shape[1]))
            line = seg[:-1:thin,:]
        else:
            #line = np.zeros((seg.shape[0]/int(thin), seg.shape[1]))
            line = seg[::thin,:]

        print line.shape
        points.append(line)

    return points

if __name__ == "__main__":

    N = 100
    axis = np.arange(N)
    arr1 = np.zeros((N,N))
    arr2 = np.zeros((N,N))

    inds1 = ((axis-N/2)**2)[:,None] + ((axis-N/2)**2)[None,:] < (N/3)**2
    inds2 = ((axis-N/2)**2)[:,None] + ((axis-N/2)**2)[None,:] < (N/3*1.1)**2
    arr1[inds1] = 1
    arr2[inds2] = 1

    arr1[10,10] = 1
    arr1[11,11] = 1
    arr1[10,11] = 1
    arr1[9,11] = 1
    arr1[10,12] = 1

    plt.imshow(arr1)
    plt.show()

    edge1 = findEdges(arr1)

    plt.imshow(edge1)
    plt.show()
    edge2 = findEdges(arr2)
    points = genBoundaryPoints(arr1, thin=3)
    plt.show()

    for line in points:
        X = line[:,0]
        Y = line[:,1]

        print line[0], line[-1]
        plt.plot(X,Y)
    plt.show()
