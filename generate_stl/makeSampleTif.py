from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def makeSphereFiles(N=100):

    dat = np.zeros((N,N,N), dtype=np.uint8)

    ax = np.arange(N)
    X, Y, Z = np.meshgrid(ax, ax, ax)

    C = N/2
    R2 = (N/3) ** 2

    inds = (X-C)**2 + (Y-C)**2 + (Z-C)**2 < R2
    dat[inds] = 255

    for i in xrange(N):
        arr = dat[i,:,:]
        im = Image.fromarray(arr)
        print im.mode, im.size
        im.save("SPHERE_{0:03d}.TIF".format(i))

if __name__ == "__main__":

    makeSphereFiles(N=100)

