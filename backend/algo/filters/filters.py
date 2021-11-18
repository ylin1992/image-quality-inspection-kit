import numpy as np
import abc

class FrequencyDomainFilter(abc.ABC):
    @abc.abstractmethod
    def __init__(self, **kwargs):
        pass
    
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

    @abc.abstractmethod
    def set_shape(self, shape):
        return NotImplemented
    
    @abc.abstractmethod
    def get_shape(self):
        return NotImplemented
    
    @abc.abstractmethod
    def set_frequency_para(self, para):
        return NotImplemented
    
    @abc.abstractmethod
    def get_frequency_para(self):
        return NotImplemented
    
    @abc.abstractmethod
    def set_filter_type(self):
        return NotImplemented
    
    @abc.abstractmethod
    def get_filter_type(self):
        return NotImplemented
        
    