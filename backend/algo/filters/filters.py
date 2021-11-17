import numpy as np
import abc

class Filter(abc.ABC):
    @abc.abstractmethod
    def __init__(self, **kwargs):
        self.__filt = None
        if 'type' in kwargs:
            if kwargs['type'] == 'bp' and 'cutoff' not in kwargs:
                raise ValueError("Please check your input: cutoff freq is essential for bp filter")
            if kwargs['type'] != 'bp' and kwargs['type'] != 'lp' and kwargs['type'] != 'hp':
                raise ValueError("Please check your input type, bp, lp or hp")
    
    @abc.abstractmethod
    def get_filt(self):
        return NotImplemented
    
    @abc.abstractmethod
    def low_pass(self, shape, cutoff):
        return NotImplemented
    
    @abc.abstractmethod
    def high_pass(self, shape, cutoff):
        return NotImplemented

    @abc.abstractmethod
    def band_pass(self, shape, cutin, cutoff):
        return NotImplemented
    
    @abc.abstractmethod
    def apply(self, image):
        return NotImplemented

    
    
