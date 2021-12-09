import numpy as np
import abc
from backend.algo.filters.filters import FrequencyDomainFilter

class GaussianFilter(FrequencyDomainFilter):
    def __init__(self, shape, sigma_x, sigma_y, type='bp', sigma_x2=None, sigma_y2=None):
        self.__sigma_x = None
        self.__sigma_x2 = None
        self.__sigma_y = None
        self.__sigma_y2 = None
        if type == 'bp' and (sigma_x2 is None or sigma_y2 is None):
            raise ValueError("Bandpass filter needs sigma_x2 and sigma_y2")
        self.set_frequency_para(sigma_x, sigma_y, sigma_x2, sigma_y2)
        self.set_shape(shape)
        self.set_filter_type(type)
        self.gen_filt()
        
    def get_filt(self):
        return self.__filt
    
    def low_pass(self, shape, sigma_x, sigma_y, cx=0, cy=0):
        rows, cols = shape
        x = np.linspace(-0.5, 0.5, cols)[np.newaxis]
        y = np.linspace(-0.5, 0.5, rows)[:, np.newaxis]
        sx = sigma_x# * cols
        sy = sigma_y #* rows
        return np.exp( -( (x-cx)**2 / (2*sx**2) ) - ( (y-cy)**2 / (2*sy**2) ))
    
    def gen_filt(self):
        if self.__type == 'bp':
            self.__filt = self.band_pass()
        elif self.__type == 'lp':
            self.__filt = self.low_pass(self.__shape, self.__sigma_x, self.__sigma_y)
        elif self.__type == 'hp':
            self.__filt = self.high_pass()
        else:
            raise ValueError("Invalid type: " + type)
    
    def high_pass(self):
        return 1 - self.low_pass(self.__shape, self.__sigma_x2, self.__sigma_y2)

    def band_pass(self):
        if self.__sigma_x is None or self.__sigma_x2 is None or self.__sigma_y is None or self.__sigma_y2 is None:
            raise ValueError("Sigmas haven't been intiated")
        return self.low_pass(self.__shape, self.__sigma_x2, self.__sigma_y2) - self.low_pass(self.__shape, self.__sigma_x, self.__sigma_y)
        
    def apply(self, image):
        if self.__filt is not None:
            if self.__filt.shape != image.shape:
                raise ValueError("Mismatch shape")
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
    
    def get_shape(self, shape):
        if shape is None or len(shape) != 2:
            raise ValueError("Shape is invalid")
        self.__shape = shape
        
        
    def set_frequency_para(self, sigma_x, sigma_y, sigma_x2=None, sigma_y2=None):
        if sigma_x is not None:
            if sigma_x is None and type(sigma_x) is not int and type(sigma_x) is not float:
                raise ValueError("sigma_x is invalid")
            self.__sigma_x = sigma_x + 1e-6

        if sigma_y is not None:
            if sigma_y is None and type(sigma_y) is not int and type(sigma_y) is not float:
                raise ValueError("sigma_y is invalid")
            self.__sigma_y = sigma_y + 1e-6
            
        if sigma_x2 is not None:
            if sigma_x2 is None and type(sigma_x2) is not int and type(sigma_x2) is not float:
                raise ValueError("cutin is invalid")
            self.__sigma_x2 = sigma_x2 + 1e-6

        if sigma_y2 is not None:
            if sigma_y2 is None and type(sigma_y2) is not int and type(sigma_y2) is not float:
                raise ValueError("cutin is invalid")
            self.__sigma_y2 = sigma_y2 + 1e-6
        
    def get_frequency_para(self):
        return {
            'sigma_x': self.__sigma_x,
            'sigma_y': self.__sigma_y,
            'sigma_x2': self.__sigma_x2 if self.__sigma_x2 is not None else None,
            'sigma_y2': self.__sigma_y2 if self.__sigma_y2 is not None else None
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