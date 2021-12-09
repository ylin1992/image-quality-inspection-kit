from .filters import FrequencyDomainFilter
import numpy as np
class ButterworthFilter(FrequencyDomainFilter):
    def __init__(self, shape, cutin=None, cutoff=None, type='bp'):
        if type == 'bp' and (cutin is None and cutoff is None):
            raise ValueError("Bandpass filter needs both cutin and cutoff")
        if type == 'lp' or type == 'hp':
            if cutin is None:
                raise ValueError("Specify cutin for lowpass and high pass filter")
        self.set_frequency_para(cutin, cutoff)
        self.set_shape(shape)
        self.set_filter_type(type)
        self.gen_filt()
    
    def gen_filt(self):
        if self.__type == 'bp':
            self.__filt = self.band_pass(self.__shape, self.__cutin, self.__cutoff)
        elif self.__type == 'lp':
            self.__filt = self.low_pass(self.__shape, self.__cutin)
        elif self.__type == 'hp':
            self.__filt = self.high_pass(self.__shape, self.__cutin)
        else:
            raise ValueError("Invalid type: " + type)
        
    def low_pass(self, shape, cutoff, x_as=1, y_as=1):
        cutoff += 1e-6
        rows, cols = shape
        x = np.linspace(-0.5, 0.5, cols)
        y = np.linspace(-0.5, 0.5, rows)
        radius = np.sqrt(((x * x_as) ** 2)[np.newaxis] + ((y * y_as) ** 2)[:, np.newaxis])
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
        
    def get_filt(self):
        return self.__filt    
        
    def set_shape(self, shape):
        if shape is None or len(shape) != 2 or type(shape) is not tuple:
            raise ValueError("Invalid shape")
        self.__shape = shape
    
    def get_shape(self):
        return self.__shape
        
    def set_frequency_para(self, cutin, cutoff):
        if cutin is not None:
            if cutin is None and type(cutin) is not int and type(cutin) is not float:
                raise ValueError("cutin is invalid")
            self.__cutin = cutin

        if cutoff is not None:
            if cutoff is None and type(cutoff) is not int and type(cutoff) is not float:
                raise ValueError("cutin is invalid")
            self.__cutoff = cutoff
        
    def get_frequency_para(self):
        return {
            'cutin': self.__cutin,
            'cutoff': self.__cutoff
        }
    
    def set_filter_type(self, _type):
        if _type is None:
            raise ValueError("type is None")
        if type(_type) is not str:
            raise TypeError("type should be a string")
        if _type != 'bp' and _type != 'lp' and _type != 'hp':
            raise ValueError('type should be one of "bp", "hp", "lp"')
        self.__type = _type
    
    def get_filter_type(self):
        return self.__type
    

    
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
