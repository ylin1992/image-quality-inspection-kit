import numpy as np
import cv2

from algo.filters.butterworth import ButterworthFilter
from algo.stain_detection.blemish_detection import BlemishDetection

import matplotlib.pyplot as plt
def test():
    image = cv2.imread('white_1x.png', 0)
    shape = image.shape
    filt = ButterworthFilter(shape=shape, cutin=0.01, cutoff=0.1, type='bp')
    blm = BlemishDetection(_filter=filt, image=image)
    print("Has image: ", blm.has_image())
    print("Mode: ", blm.get_mode())
    print("Has filter: ", blm.has_filter())
    res = blm.start_calculate(thr=1.0)
    plt.figure()
    plt.imshow(res)
    '''
    @TODO: add test for set filter, set para
    '''
    
    filt2 = ButterworthFilter(shape=shape, cutin=0.2, cutoff=0.5, type='bp')
    blm.set_para(_filter=filt2)
    res2 = blm.start_calculate(thr=1.0)
    plt.figure()
    plt.imshow(res2)
    plt.show()
test()