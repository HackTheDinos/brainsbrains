#!/usr/bin/env python

import sys
from PIL import Image
import numpy as np
import h5py as h5

def loadImArray(filename):
    im = Image.open(filename)
    print filename, im.size, im.mode, im.format
    w, h = im.size
    data = im.getdata()
    arr = np.array(data)
    arr = arr.reshape((h,w))

    
    arr8 = arr.astype(np.uint8)

    #im.show()

    return arr8

if __name__ == "__main__":

    ims = []

    for f in sys.argv[1:]:
        im = Image.open(f)
        im.show()

