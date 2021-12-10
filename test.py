from backend.service import DetectionService
from backend.service import FilterService
import cv2
import matplotlib.pyplot as plt

im = cv2.imread('./backend/blm_20000.png', 0)
shape = im.shape
filter = FilterService.get_butterworth_filter(shape=shape, cutin=0.03, cutoff=0.5, type='bp')
blm = DetectionService.getBlemishDetection(im, filter, ref_image=im, ratio=0.99, roi_w=100)
res, thr_map = blm.start_calculate(0.05)
plt.figure()
plt.imshow(res)
plt.figure()
plt.imshow(thr_map)
plt.show()