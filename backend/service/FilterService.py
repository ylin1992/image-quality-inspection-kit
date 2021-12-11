from backend.algo.filters.log import LaplacianOfGaussianFilter
from backend.algo.filters.butterworth import ButterworthFilter
from backend.algo.filters.gaussian import GaussianFilter
from backend.algo.filters.filters import FrequencyDomainFilter

def get_gaussian_filter(shape, sigma_x, sigma_y, type='lp', sigma_x2=0, sigma_y2=0):
    print(shape, sigma_x, sigma_y, type, sigma_x2, sigma_y2)
    try:
        filt = GaussianFilter(shape=shape, sigma_x=sigma_x, sigma_y=sigma_y, type=type, sigma_x2=sigma_x2, sigma_y2=sigma_y2)
        return filt
    except Exception as e:
        print(e)
        return None


def get_butterworth_filter(shape, cutin, cutoff=0, type='bp'):
    print(shape, cutin, cutoff, type)
    try:
        filt = ButterworthFilter(shape=shape, cutin=cutin, cutoff=cutoff, type=type)
        return filt
    except Exception as e:
        print(e)
        return None

def get_filter_shape(filter: FrequencyDomainFilter):
    return filter.get_shape()