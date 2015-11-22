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

def genBoundaryPoints(im, thin=1, dn=10):
    
    Ny, Nx = im.shape

    axX = np.arange(Nx)
    axY = np.arange(Ny)

    X, Y = np.meshgrid(axX, axY)

    fig, ax = plt.subplots()
    C = ax.contour(X, Y, im, levels=[0.5*(im.max()+im.min())])
    plt.close()

    segs = C.allsegs[0]

    points = []

    #plt.figure()

    for seg in segs:
        #print seg.shape

        #plt.plot(seg[:,0], seg[:,1])

        if (seg[:,0]<dn).any() or (seg[:,0]>Nx-dn-1).any() or\
                (seg[:,1]<dn).any() or (seg[:,1]>Ny-dn-1).any() or\
                seg.shape[0] < 3:
            continue

        seg = seg[:-1,:]
        line = seg[::thin,:].copy()

        #print line[:,0].min(), line[:,0].max(), line[:,1].min(), line[:,1].max()
        points.append(line)

    #plt.show()

    return points

def loadImage(filename):
    im0 = Image.open(filename)
    im = im0.convert("L")
    print filename, im.size, im.mode, im.format
    w, h = im.size
    data = im.getdata()
    arr = np.array(data)
    arr = arr.reshape((h,w))
    arr8 = arr.astype(np.uint8)

    return arr8

def genTriangles(bp1, bp2, k1, k2):

    #TODO: Make work on Windows
    lib = ctypes.cdll.LoadLibrary('libtriangle.so')
    cGenTri = lib.buildTwoLayerTriangles
    cGenTri.argtypes = [ndpointer(ctypes.c_int), 
                        ndpointer(ctypes.c_int), ctypes.c_int, ctypes.c_int,
                        ndpointer(ctypes.c_int), ctypes.c_int, ctypes.c_int]

    len1 = np.array([bp.shape[0] for bp in bp1])
    len2 = np.array([bp.shape[0] for bp in bp2])
    ind1 = np.argsort(len1)
    ind2 = np.argsort(len2)
    i1 = ind1[-1]
    i2 = ind2[-1]

    BP1 = (2*bp1[i1]).astype(np.int32)
    BP2 = (2*bp2[i2]).astype(np.int32)

    dist = ((BP1[0]-BP2)*(BP1[0]-BP2)).sum(axis=1)
    ind = np.argmin(dist)
    BP2 = np.roll(BP2, -ind, axis=0)

    n1 = BP1.shape[0]
    n2 = BP2.shape[0]

    BP1 = BP1.reshape(2*n1)
    BP2 = BP2.reshape(2*n2)

    triangles = np.ascontiguousarray(np.zeros((n1+n2)*3*3, dtype=np.int32))

    cGenTri(    triangles,
                np.ascontiguousarray(BP1,dtype=np.int32), n1, 2*k1,
                np.ascontiguousarray(BP2,dtype=np.int32), n2, 2*k2)

    triangles = triangles.reshape((n1+n2,3,3))

    """
    tri1 = [ [0,0,0],[1,0,0],[0,1,0]]
    tri2 = [ [0,0,0],[1,0,0],[0,0,1]]
    tri3 = [ [0,0,0],[0,0,1],[0,1,0]]
    tri4 = [ [1,0,0],[0,1,0],[0,0,1]]

    return np.array([tri1, tri2, tri3, tri4])
    """
    return triangles

def makeStlStrip(outfile, bp1, bp2, k1, k2):

    if bp1 is None and bp2 is None:
        return
    elif bp1 is None and bp2 is not None:
        triangles = genSurfaceTriangles(bp2, k2, 1.0)
    elif bp1 is not None and bp2 is None:
        triangles = genSurfaceTriangles(bp1, k1, -1.0)
    else:
        triangles = genTriangles(bp1, bp2, k1, k2)

    f = open(outfile, "a")
    for tri in triangles:
        printStlTriangle(f, tri)
    f.close()

def genSurfaceTriangles(bp, k, scale):
    
    lenarr = np.array([ibp.shape[0] for ibp in bp])
    inds = np.argsort(lenarr)
    i1 = inds[-1]

    BP = bp[i1]

    xc = BP[:,0].mean()
    yc = BP[:,1].mean()

    vc = np.array([xc, yc, k])

    triangles = []

    for i in xrange(-1,BP.shape[0]-1):
        va = np.array([BP[i,0], BP[i,1], k])
        vb = np.array([BP[i+1,0], BP[i+1,1], k])
        if scale > 0:
            tri = 2*np.array([va, vb, vc])
        else:
            tri = 2*np.array([vb, va, vc])
        triangles.append(tri)

    return np.array(triangles)


def printStlTriangle(f, tri):
    va = (tri[1]-tri[0]).astype(np.float)
    vb = (tri[2]-tri[0]).astype(np.float)
    vn = np.cross(va, vb)
    norm  = math.sqrt((vn*vn).sum())
    vn /= norm
    if norm <= 0.0:
        print "BAD"
        print tri
        return
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
    return

def prepStlFile(outfile):
    f = open(outfile, "w")
    f.write("solid brain\n")
    f.close()

def finishStlFile(outfile):
    f = open(outfile, "a")
    f.write("endsolid brain\n")
    f.close()

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("usage: stack2stl.py thin out [images ...]")
        print("    Creates .stl file from image stacks.")
        sys.exit()

    thin = int(sys.argv[1])
    outname = sys.argv[2]

    prepStlFile(outname)

    slices = range(3, len(sys.argv)-1, thin)

    i2 = slices[0]
    file2 = sys.argv[i2]
    im2 = loadImage(file2)
    bp2 = genBoundaryPoints(im2, thin=thin)
    bp1 = None
    makeStlStrip(outname, bp1, bp2, -1, i2)

    for i in xrange(len(slices)-1):
        i1 = slices[i]
        i2 = slices[i+1]
        file1 = sys.argv[i1]
        file2 = sys.argv[i2]
        im1 = loadImage(file1)
        im2 = loadImage(file2)
        bp1 = genBoundaryPoints(im1, thin=thin)
        bp2 = genBoundaryPoints(im2, thin=thin)

        if len(bp1) < 3:
            bp1 = None
        if len(bp2) < 3:
            bp2 = None
        makeStlStrip(outname, bp1, bp2, i1, i2)

    i1 = slices[-1]
    file1 = sys.argv[i1]
    im1 = loadImage(file1)
    bp1 = genBoundaryPoints(im1, thin=thin)
    bp2 = None
    makeStlStrip(outname, bp1, bp2, i1, -1)

    finishStlFile(outname)



