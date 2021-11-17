from .filters import Filter
import numpy as np
class ButterworthFilter(Filter):
    
    def __init__(self, shape, cutin, **kwargs):
        super().__init__(**kwargs)
        if kwargs['type'] == 'bp':
            self.__filt = self.band_pass(shape, cutin, kwargs['cutoff'])
        elif kwargs['type'] == 'lp':
            self.__filt = self.low_pass(shape, cutin)
        else:
            self.__filt = self.high_pass(shape, cutin)
    
    def get_filt(self):
        return self.__filt
    
    def low_pass(self, shape, cutoff, x_as=1, y_as=1):
        cutoff += 1e-6
        rows, cols = shape
        x = np.linspace(-0.5, 0.5, cols)
        y = np.linspace(-0.5, 0.5, rows)
        # alpha = np.deg2rad(60)
        # x_rot = x * np.sin(alpha) - y * np.cos(-alpha)
        # y_rot = x * np.sin(-alpha) + y * np.cos(alpha)
        radius = np.sqrt(((x * x_as) ** 2)[np.newaxis] + ((y * y_as) ** 2)[:, np.newaxis])
        # c, s = np.cos(-alpha), np.sin(-alpha)
        # R = np.array(((c, -s), (s, c)))
        # radius = np.dot()
        filt = 1 / (1.0 + (radius / cutoff) ** (2))
        return filt
    
    def high_pass(self, shape, cutoff):
        return 1 - self.low_pass(shape, cutoff)

    def band_pass(self, shape, cutin, cutoff):
        return self.low_pass(shape, cutoff) - self.low_pass(shape, cutin)
    
    def apply(self, image):
        if self.__filt is not None:
            fft_orig = np.real(np.fft.fftshift(np.fft.fft2(image)))
            fft_orig *= self.__filt
            filtered = np.abs(np.fft.ifft2(np.fft.ifftshift(fft_orig)))
            return filtered
        else:
            print("Initialize the filter first")
            return None
def butter2d_lp(shape, f, n):
    rows, cols = shape
    x = np.linspace(-0.5, 0.5, cols) * cols
    y = np.linspace(-0.5, 0.5, rows) * rows
    radius = np.sqrt((x ** 2)[np.newaxis] + (y ** 2)[:, np.newaxis])
    filt = 1 / (1.0 + (radius / f) ** (2 * n))
    return filt


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import cv2
    
    im = cv2.imread('white_1x.png', 0)
    shape = im.shape
    btw_filter = ButterworthFilter(shape=shape, cutin=0.02, cutoff=0.3, type='bp')
    print("Sum: ", np.sum(btw_filter.get_filt()))
    plt.figure()
    plt.imshow(im)
    plt.figure()
    plt.imshow(btw_filter.get_filt())
    plt.figure()
    plt.imshow(btw_filter.apply(im))
    plt.show()
