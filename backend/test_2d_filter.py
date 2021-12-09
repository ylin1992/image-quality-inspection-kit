import numpy as np
import cv2
from scipy.signal import convolve2d
import matplotlib.pyplot as plt

im = cv2.imread("white_1x.png", 0)
circles = cv2.HoughCircles(im,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=40,maxRadius=80)

print(circles)
cimg = cv2.cvtColor(im,cv2.COLOR_GRAY2BGR)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
    cv2.putText(cimg, str(i[2]), (i[0], i[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
# kernel_stretch = np.array([[1,1,1], [1,-8,1], [1,1,1]])
# kernel_1st_der = np.array([[0,1,0], [1,-4,1], [0,1,0]])
# kernel_sharpen = kernel_stretch * -1

# f1 = convolve2d(im, kernel_1st_der, boundary='symm', mode='same')
# f2 = np.zeros_like(f1, dtype=np.uint8)
# f2[f1 > 50] = 255
plt.figure()
plt.imshow(cimg)
plt.show()

# conv = np.convolve(im, kernel)
# conv = convolve(im, kernel)