from backend.algo.stain_detection import blemish_detection
from backend.algo.stain_detection.blemish_detection import BlemishDetection
from backend.algo.filters.filters import FrequencyDomainFilter

def getBlemishDetection(image, filter: FrequencyDomainFilter, ref_image=None, ratio=None, roi_w=None):
    if image is None:
        return None
    blm = None
    try:
        if ref_image is None:
            blm = BlemishDetection(image, filter)
        else:
            blm = BlemishDetection(image, filter, ref_image, ratio, roi_w)
    except Exception as e:
        print(e)
        raise e
    return blm

