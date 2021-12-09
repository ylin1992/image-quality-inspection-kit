from backend.algo.filters.log import LaplacianOfGaussianFilter
from backend.algo.filters.butterworth import ButterworthFilter
from backend.algo.filters.gaussian import GaussianFilter
from backend.algo.filters.filters import FrequencyDomainFilter

def get_gaussian_filter(shape, sigma_x, sigma_y, type='lp', sigma_x2=0, sigma_y2=0):
    g = GaussianFilter(shape=shape, sigma_x=0.1, sigma_y=0.1, type='lp')
    g2 = GaussianFilter(shape=shape, sigma_x=0.1, sigma_y=0.1, type='bp', sigma_x2=0.8, sigma_y2=0.8)
    g3 = GaussianFilter(shape=shape, sigma_x=0.1, sigma_y=0.1, type='lp', sigma_x2=0.8, sigma_y2=0.8)


def get_butterworth_filter(shape, cutin, cutoff=0, type='bp'):
    print(shape, cutin, cutoff, type)
    try:
        filt = ButterworthFilter(shape=shape, cutin=cutin, cutoff=cutoff, type=type)
        return filt
    except Exception as e:
        print(e)
        return None
