from multiprocessing.sharedctypes import Value
from typing import overload
from algo.filters.gaussian import GaussianFilter
import numpy as np

class LaplacianOfGaussianFilter(GaussianFilter):

    def __init__(self, shape, sigma_x, sigma_y, type='bp', dir='v', sigma_x2=None, sigma_y2=None):
        self.__dir = None
        self.set_dir(dir)
        super().__init__(shape, sigma_x, sigma_y, type=type, sigma_x2=sigma_x2, sigma_y2=sigma_y2)
        
    def low_pass(self, shape, sigma_x, sigma_y, cx=0, cy=0):
        rows, cols = shape

        sx = sigma_x# * cols
        sy = sigma_y #* rows
        if self.__dir == 'dot':
            x = np.linspace(-0.5, 0.5, cols)[np.newaxis]
            y = np.linspace(-0.5, 0.5, rows)[:, np.newaxis]
            order = -( (x-cx)**2 / (2*sx**2) ) - ( (y-cy)**2 / (2*sy**2))
            a = -1 / (np.pi * (sx + sy) **4)
        elif self.__dir == 'v':
            x = np.linspace(-0.5, 0.5, cols)[np.newaxis]
            y = np.ones(rows)[:, np.newaxis]
            order = -(((x-cx)**2 + (y-cy)**2) / 2 * sigma_x**2)
            a = -1 / (np.pi * (sx) **4)
        elif self.__dir == 'h':
            x = np.ones(cols)[np.newaxis]
            y = np.linspace(-0.5, 0.5, rows)[:, np.newaxis]
            order = -(((x-cx)**2 + (y-cy)**2) / 2 * sigma_x**2)
            a = -1 / (np.pi * (sx) **4)
        else:
            raise ValueError("Invalid dir: ", self.__dir)
        b = 1 - order
        exp = np.exp(order)
        return a * b * exp
    
    def set_dir(self, dir):
        if dir is None:
            raise ValueError("Invalid dir: ", dir)
        if type(dir) is not str:
            raise TypeError("Invalid type of direction")
        if dir not in ['v', 'h', 'dot']:
            raise ValueError("Invalid direction (must be in 'v', 'h', 'dot')")
        self.__dir = dir
        
    def get_frequency_para(self):
        d = super().get_frequency_para()
        d['dir'] = self.__dir
        return d