from backend.algo.stain_detection import blemish_detection
from backend.algo.stain_detection.blemish_detection import BlemishDetection
from backend.algo.filters.filters import FrequencyDomainFilter

class BlemishDetectionService:
    def __init__(self, image=None, filter=None, ref_image=None, ratio=None, roi_w=None):
        self._image = image
        self._filter = filter
        self._ref_image = ref_image
        self._ratio = ratio
        self._roi_w = roi_w

        self._blm = None
        self._dual_mode = False
        if self._ref_image is not None:
            self._dual_mode = True

        try:
            self.createBlemishDetectionObject()
        except:
            pass

    def createBlemishDetectionObject(self):
        if self._image is None:
            raise ValueError("Image is not loaded")
        
        if self._filter is None:
            raise ValueError("Filter is not loaded")

        if self._filter.get_shape() != self._image.shape:
            raise ValueError("Invalid shape of image or filter, please check dimensions")

        try:
            if self._dual_mode:
                self._blm = BlemishDetection(self._image, self._filter, self._ref_image, self._ratio, self._roi_w)
            else:
                self._blm = BlemishDetection(self._image, self._filter)
        except Exception as e:
            print(e)
            raise e

    def start_calculate(self, thr):
        if self._blm is None:
            raise ValueError("Blm object is not created")
        
        res, map = self._blm.start_calculate(thr)
        return res, map

    def resetAll(self):
        self._image = None
        self._filter = None
        self._ref_image = None
        self._ratio = None
        self._row_w = None

        self._blm = None

    def set_image(self, image):
        self._image = image
    
    def set_filter(self, filter):
        self._filter = filter

    def set_ref_image(self, ref_image):
        if ref_image is not None:
            self._dual_mode = True
        else:
            self._dual_mode = False
        self._ref_image = ref_image

    def set_ratio(self, ratio):
        self._ratio = ratio

    def set_roi_w(self, roi_w):
        self._roi_w = roi_w

    def get_image(self):
        return self._image
    
    def get_filter(self):
        return self._filter
    
    def get_ref_image(self):
        return self._ref_image

    def get_ratio(self):
        return self._ratio

    def get_roi_w(self):
        return self._roi_w

    def get_blm(self):
        return self._blm

    def get_filtered_target_image(self):
        return self._blm.get_filtered_target_image()

    def get_filtered_ref_image(self):
        return self._blm.get_filtered_ref_image()