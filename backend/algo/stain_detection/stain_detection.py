import abc
from backend.algo.filters.filters import FrequencyDomainFilter


class StainDetection(abc.ABC):
    @abc.abstractmethod
    def start_calculate(self):
        return NotImplemented
    
    @abc.abstractmethod
    def has_image(self):
        return self.__image is not None
    
    @abc.abstractmethod
    def set_image(self):
        return NotImplemented
    
    @abc.abstractmethod
    def get_image(self):
        return self.__image
    
    @abc.abstractmethod
    def get_filter(self):
        return self.__filter
    
    @abc.abstractmethod
    def set_filter(self):
        if not issubclass(filter.__class__, FrequencyDomainFilter):
            raise ValueError("Make sure to input a valid Filter object")
        self.__filter = filter
        
    @abc.abstractmethod
    def set_para(self, **kwargs):
        return NotImplemented