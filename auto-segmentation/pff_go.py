"""General strategy:

- Start with a nicely segmented image in the stack and an x,y
  coordinate which identifies the segment of interest (the brain).

- Create an initial boolean array, called "mask" which is True in the
  region of interest, False otherwise.

- Segment adjacent image, each having a unique greyscale value
  identifier, and select the segment that is most similar -- in terms
  of image array difference -- the "mask".

- If a satisfactorily similar segment is found, set it to be the mask
  and continue to next image.

- If no satisfactory match, repeat segmentation with a small change in
  graphical segmentation parameters (smoothing length sigma)

- After searching parameters, if no satisfactory match is found, keep
  mask the same and move on to the next image

Team "Brainbuilders" and "Pterodata"

"""


import cv2
import numpy
import tempfile
import subprocess
from functools import partial
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import matplotlib.image as mpimg
import numpy as np
import scipy.ndimage as nd
from PIL import Image


def pff(filename, sigma, k, m):
    
    f_ppm = tempfile.NamedTemporaryFile(suffix='.ppm')
    subprocess.check_call(
        ['convert', filename, f_ppm.name]
    )

    f_seg = tempfile.NamedTemporaryFile(suffix='.ppm')
    subprocess.check_call(
        ('./segment %f %d %d %s %s' % (sigma, k, m, f_ppm.name, f_seg.name)).split()
    )

    f_out = tempfile.NamedTemporaryFile(suffix='.png')
    subprocess.check_call(
        ['convert', f_seg.name, f_out.name]
    )

    img = nd.imread(f_out.name)
    return img

def match(mask,img):
    """Compare mask and the current, segmented, image.  Take the absolute
    sum difference (L1) between the mask and segments.

    """
    uniques = np.unique(img)
    costs = np.array([(np.abs((img==u).astype(int)-mask.astype(int)).sum()) for u in uniques])
    pos = np.where(costs==np.amin(costs))
    pos = np.amin(pos) # NB: sometimes there are duplicate costs
    newmask = img == uniques[pos]
    return newmask

def gen_img_fname(inp_dir, species, form, frame):
    return '%s/%s%04d.%s' % (inp_dir, species, frame, form)

def run(inp_dir, species,
        start_frame, end_frame,
        init_x, init_y,
        out_dir,
        should_add_orig, leave_garbage):

    print "generating initial mask"
    inp_frame = partial(gen_img_fname, inp_dir, species, 'tif')
    #mask = pff(inp_frame(start_frame), 0.7, 500, 20)
    mask = pff(inp_frame(start_frame), 0.1, 500, 40)
    mask = mask == mask[init_x, init_y]

    out_frame = partial(gen_img_fname, out_dir, species, 'tif')

    if end_frame > start_frame:
        step = 1
    else:
        step = -1

    for f in xrange(start_frame + step, end_frame + step, step):
        print
        print "generating mask %d" % f

        # we really don't know what we're doing

        # search for smoothing factor that doesn't lead to
        # discontinous brains
        #sigmas = [0.8, 1.0, 1.1]
        sigmas = [0.1, 0.2, 0.3]

        for sigma in sigmas:
            Vol=mask.astype(int).sum()
            print "VOL", Vol

            print 'trying sigma %f' % sigma
            #seg_img = pff(inp_frame(f), sigma, int(200 / sigma), 20)
            seg_img = pff(inp_frame(f), sigma, 500, 40)
            new_mask = match(mask, seg_img)

            #is_bad_mask = cost / mask.astype(int).sum() > 0.3
            newVol=new_mask.astype(int).sum()
            is_bad_mask = (newVol < 0.5 *Vol) or (newVol > 10.*Vol)

            if not is_bad_mask:
                break

        #is_bad_mask *= new_mask.astype(int).sum() > 2.0 * mask.astype(int).sum()
        if is_bad_mask:
            print "skipping %d" % f

            if leave_garbage:
                # save out the segmented image so we can see how bad it is
                # plt.imshow(seg_img)
                # plt.savefig(out_frame(f))
                new_mask = mask
            else:
                continue

        new_mask = nd.binary_dilation(new_mask)
        new_mask = nd.binary_erosion(new_mask)

        print "areas", mask.astype(int).sum(), new_mask.astype(int).sum()

        print "outputting", out_frame(f)

        if should_add_orig:
            fig = plt.figure()

            fig.add_subplot(1, 2, 1)
            plt.imshow(new_mask)

            fig.add_subplot(1, 2, 2)
            plt.imshow(cv2.imread(inp_frame(f)))

            plt.savefig(out_frame(f))
        else:
            fig = plt.imshow(new_mask, cmap = cm.Greys_r)
            fig.axes.get_xaxis().set_visible(False)
            fig.axes.get_yaxis().set_visible(False)
            plt.savefig(out_frame(f))
        
        mask = new_mask

if __name__ == '__main__':
    import sys

    if sys.argv[1] == 'f':
        #start_frame, end_frame = 1202, 1426
        #init_x, init_y = 100, 400
        start_frame, end_frame = 1100, 1160
        init_x, init_y = 185, 360
    elif sys.argv[1] == 'b':
        start_frame, end_frame = 1145, 1050
        init_x, init_y = 100, 400
    else:
        raise ValueError("NO")

    run(
        inp_dir='Hackathon_CTdata/Gavia/8bit',
        species='gavia',
        start_frame=start_frame, # [1050, 1426]
        end_frame=end_frame,
        init_x=init_x,
        init_y=init_y,
        out_dir='pff_go_out/gavia',
        should_add_orig=True,
        leave_garbage=True,
    )
