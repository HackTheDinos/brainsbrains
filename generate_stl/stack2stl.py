#!/usr/bin/env python

import sys
import ctypes
import numpy as np
import matplotlib.pyplot as plt
from skimage import feature
from PIL import Image

def findEdges(im):

    edges = feature.canny(im)
    return edges

def genBoundaryPoints(im, thin=1):
    
    Ny, Nx = im.shape

    axX = np.arange(Nx)
    axY = np.arange(Ny)

    X, Y = np.meshgrid(axX, axY)

    fig, ax = plt.subplots()
    C = ax.contour(X, Y, im, levels=[0.5*(im.max()+im.min())])
    plt.close()

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

        points.append(line)

    return points

def loadImage(filename):
    im = Image.open(filename)
    print filename, im.size, im.mode, im.format
    w, h = im.size
    data = im.getdata()
    arr = np.array(data)
    arr = arr.reshape((h,w))
    arr8 = arr.astype(np.uint8)

    return arr8

def genTriangles(bp1, bp2, k):

    #TODO: Make work on Windows
    lib = ctypes.cdll.LoadLibrary('libtriangle.so')
    cGenTri = lib.buildTwoLayerTriangles

    BP1 = (2*bp1[0]).astype(np.int32)
    BP2 = (2*bp2[0]).astype(np.int32)

    dist = ((BP1[0]-BP2)*(BP1[0]-BP2)).sum(axis=1)
    ind = np.argmin(dist)
    print ind, BP1[0], BP2[0]
    BP2 = np.roll(BP2, -ind, axis=0)

    print ind, BP1[0], BP2[0]

    n1 = BP1.shape[0]
    n2 = BP2.shape[0]
    triangles = np.zeros((n1+n2,3,3), dtype=np.int32)

    cGenTri(    ctypes.c_void_p(triangles.ctypes.data),
                ctypes.c_void_p(BP1.ctypes.data),
                n1, k,
                ctypes.c_void_p(BP2.ctypes.data),
                n2, k+1)

    """
    tri1 = [ [0,0,0],[1,0,0],[0,1,0]]
    tri2 = [ [0,0,0],[1,0,0],[0,0,1]]
    tri3 = [ [0,0,0],[0,0,1],[0,1,0]]
    tri4 = [ [1,0,0],[0,1,0],[0,0,1]]

    return np.array([tri1, tri2, tri3, tri4])
    """
    return triangles

def makeStlStrip(outfile, bp1, bp2, k):
    triangles = genTriangles(bp1, bp2, k)

    f = open(outfile, "a")

    for tri in triangles:
        f.write("facet normal 0 0 0\n")
        f.write("    outer loop\n")
        f.write("        vertex {0:e} {1:e} {2:e}\n".format(
                                tri[0,0],tri[0,1],tri[0,2]))
        f.write("        vertex {0:e} {1:e} {2:e}\n".format(
                                tri[1,0],tri[1,1],tri[1,2]))
        f.write("        vertex {0:e} {1:e} {2:e}\n".format(
                                tri[2,0],tri[2,1],tri[2,2]))
        f.write("    endloop\n")
        f.write("endfacet\n")
    f.close()
    

def prepStlFile(outfile):
    f = open(outfile, "w")
    f.write("solid brain\n")
    f.close()

def finishStlFile(outfile):
    f = open(outfile, "a")
    f.write("endsolid brain\n")
    f.close()

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage: stack2stl.py [images ...]")
        print("    Creates .stl file from image stacks.")
        sys.exit()

    outname = "out.stl"

    prepStlFile(outname)

    for i in xrange(1, len(sys.argv)-1):
        file1 = sys.argv[i]
        file2 = sys.argv[i+1]
        im1 = loadImage(file1)
        im2 = loadImage(file2)
        bp1 = genBoundaryPoints(im1, thin=1)
        bp2 = genBoundaryPoints(im2, thin=1)

        if len(bp1) == 0 or len(bp2) == 0:
            continue
        makeStlStrip(outname, bp1, bp2, i)

    finishStlFile(outname)



