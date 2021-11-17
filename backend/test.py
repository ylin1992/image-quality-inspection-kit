import numpy as np
import cv2

from algo.filters.butterworth import ButterworthFilter
from algo.stain_detection.blemish_detection import BlemishDetection

import matplotlib.pyplot as plt
def test():
    image = cv2.imread('white_1x.png', 0)
    shape = image.shape
    filt = ButterworthFilter(shape=shape, cutin=0.02, cutoff=0.3, type='bp')
    blm = BlemishDetection(_filter=filt, image=image)
    print("Has image: ", blm.has_image())
    print("Mode: ", blm.get_mode())
    print("Has filter: ", blm.has_filter())
    res = blm.start_calculate(thr=1.0)
    plt.imshow(res)
    plt.show()
test()