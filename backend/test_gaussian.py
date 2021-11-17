import numpy as np
import cv2

from algo.filters.gaussian import GaussianFilter
from algo.stain_detection.blemish_detection import BlemishDetection

def test():
    shape = (100,100)
    g = GaussianFilter(shape=shape, sigma_x=0.1, sigma_y=0.1, type='lp')
    print(g.get_frequency_para())
    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow(g.get_filt())
    g2 = GaussianFilter(shape=shape, sigma_x=0.1, sigma_y=0.1, type='bp', sigma_x2=0.8, sigma_y2=0.8)
    print(g2.get_frequency_para())
    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow(g2.get_filt())    
    
    image = cv2.imread('white_1x.png', 0)
    shape = image.shape
    g3 = GaussianFilter(shape=shape, sigma_x=0.1, sigma_y=0.1, type='bp', sigma_x2=0.8, sigma_y2=0.8)
    blm = BlemishDetection(_filter=g3, image=image)
    res2 = blm.start_calculate(thr=1.0)
    plt.figure()
    plt.imshow(res2)
    plt.show()
    
test()