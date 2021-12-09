import matplotlib.pyplot as plt
import numpy as np
import cv2

image = np.zeros((100,100))
image = cv2.circle(image, (50, 50), 25, 255, 10)

ref = np.zeros_like(image)
ref = cv2.circle(ref, (50, 50), 25, 255, 10)

fft_image = np.fft.fftshift(np.fft.fft2(image))
fft_ref = np.fft.fftshift(np.fft.fft2(ref))

corr = fft_image * np.conjugate(fft_ref)
# res = np.real(np.fft.ifft2(np.fft.ifftshift(corr)))

plt.figure()
plt.imshow(image)

plt.figure()
plt.imshow(ref)
plt.figure()
plt.imshow(res)
plt.show()