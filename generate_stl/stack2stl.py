#!/usr/bin/env python

import sys
import math
import ctypes
import numpy as np
import matplotlib.pyplot as plt
from skimage import feature
from PIL import Image
from numpy.ctypeslib import ndpointer

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

        seg = seg[:-1,:]

        #if seg.shape[0] % thin == 0:
        #    line = seg[:-1:thin,:]
        #else:
        #    line = seg[::thin,:]
        line = seg[::thin,:].copy()

        for i in xrange(line.shape[0]):
            a = line[i]
            for j in xrange(i+1, line.shape[0]):
                b = line[j]
                if (a==b).all():
                    print "double"
                    print i, a
                    print j, b


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
    cGenTri.argtypes = [ndpointer(ctypes.c_int), 
                        ndpointer(ctypes.c_int), ctypes.c_int, ctypes.c_int,
                        ndpointer(ctypes.c_int), ctypes.c_int, ctypes.c_int]

    BP1 = (2*bp1[0]).astype(np.int32)
    BP2 = (2*bp2[0]).astype(np.int32)

    dist = ((BP1[0]-BP2)*(BP1[0]-BP2)).sum(axis=1)
    ind = np.argmin(dist)
    BP2 = np.roll(BP2, -ind, axis=0)

    n1 = BP1.shape[0]
    n2 = BP2.shape[0]

    BP1 = BP1.reshape(2*n1)
    BP2 = BP2.reshape(2*n2)

    triangles = np.ascontiguousarray(np.zeros((n1+n2)*3*3, dtype=np.int32))

    cGenTri(    triangles,
                np.ascontiguousarray(BP1,dtype=np.int32), n1, 2*k,
                np.ascontiguousarray(BP2,dtype=np.int32), n2, 2*k+2)

    triangles = triangles.reshape((n1+n2,3,3))

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
        va = (tri[1]-tri[0]).astype(np.float)
        vb = (tri[2]-tri[0]).astype(np.float)
        vn = np.cross(va, vb)
        norm  = math.sqrt((vn*vn).sum())
        vn /= norm
        if norm <= 0.0:
            print "BAD"
            print tri
            continue
        f.write("facet normal {0:f} {1:f} {2:f}\n".format(
                                vn[0], vn[1], vn[2]))
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



