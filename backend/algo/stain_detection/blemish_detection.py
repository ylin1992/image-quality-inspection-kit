from typing import Type
import cv2
import numpy as np
from .stain_detection import StainDetection
from backend.algo.filters.butterworth import ButterworthFilter
from backend.algo.filters.filters import FrequencyDomainFilter
from multiprocessing.pool import ThreadPool

class BlemishDetection(StainDetection):
    
    def __init__(self, image, _filter, ref_image=None, ratio=None, roi_w=None):
        self.__ref_image = None
        self.__dual_mode = False
        self.roi_w = None
        self.ratio = None
        self.filtered_target = None
        self.filtered_ref = None
        if _filter is None:
            raise ValueError("filter is None")
        if image is None:
            raise ValueError("Image is None")
        if len(image.shape) > 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        self.__filter = _filter
        self.__image = image
        if ref_image is not None and roi_w is None and ratio is None:
            raise ValueError('ref_image is found but "roi_w" or "ratio" is not found')
        

        if ref_image is not None:
            if len(ref_image.shape) > 2:
                ref_image = cv2.cvtColor(ref_image, cv2.COLOR_BGR2GRAY)
            self.__ref_image = ref_image
            self.__dual_mode = True
            self.roi_w = roi_w
            self.ratio = ratio

        
    def start_calculate(self, thr):
        '''
            dual_mode: thr acts as a lower bound of filterd image to prevent noise
                        where result[filtered_image < thr] = 0
            single_mode: thr acts as an upper bound of filtered image
                        where result[filtered_image > thr] = 255
        '''
        if not self.has_image():
            raise ValueError("Please input testing image first")
        if self.__dual_mode:
            return self.__caculate_by_ref_image(thr)
        else:
            return self.__calculate_by_target_image(thr)

    def has_image(self):
        return self.__image is not None
    
    def set_ref_image(self, ref_image, ratio, roi_w):
        # Set as dual image detection mode
        if ref_image is None:
            raise ValueError("ref_image is None")
        if len(ref_image.shape) > 2:
            ref_image = cv2.cvtColor(ref_image, cv2.COLOR_BGR2GRAY)
        self.__ref_image = ref_image
        self.__dual_mode = True
        self.ratio = ratio
        self.roi_w = roi_w
        
    def remove_ref_image(self):
        # Set as single image detection mode
        self.__ref_image = None
        self.__dual_mode = False
        self.roi_w = None
        self.ratio = None
            
    def set_filter(self, _filter):
        if _filter is not None:
            self.__filter = _filter
        else:
            raise ValueError("filter is None")
        
    def get_filter(self):
        return self.__filter
        
    def __caculate_by_ref_image(self, thr):
        if self.__ref_image is None:
            raise ValueError("Initialize with ref image first")
        if self.__ref_image.shape != self.__filter.get_filt().shape:
            raise ValueError("Mismatch between image and ref_image, ref_image: ", self.__ref_image.shape, " filter: ", self.__filter.get_filt().shape)
        if self.__image.shape != self.__filter.get_filt().shape:
            raise ValueError("Mismatch between image and image, ref_image: ", self.__image.shape, " filter: ", self.__filter.get_filt().shape)
        
        pool = ThreadPool(processes=2)
        image_result = pool.apply_async(self.__filter.apply, (self.__image, )) # tuple of args for foo
        ref_image_result = pool.apply_async(self.__filter.apply, (self.__ref_image, ))
        
        # filtered_ref = self.__filter.apply(self.__ref_image)
        # filtered_target = self.__filter.apply(self.__image)
        filtered_ref = ref_image_result.get()
        filtered_target = image_result.get()

        thr_map = self.__get_threshold_map(filtered_ref)
        res = np.zeros_like(self.__ref_image)
        res[filtered_target > thr_map] = 255
        res[filtered_target < thr] = 0

        self.filtered_ref = filtered_ref
        self.filtered_target = filtered_target
        return res, thr_map
    
    def __calculate_by_target_image(self, thr):
        self.filtered_target = self.__filter.apply(self.__image)
        res = np.zeros_like(self.__image, dtype=float)
        res[self.filtered_target > thr] = 255
        return res, None
    
    def set_image(self, image):
        if image is None:
            raise ValueError("Image is None")
        if len(image.shape) > 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.__image = image
    
    def get_image(self):
        return self.__image
        
    def __get_threshold_map(self, image, thr=0):
        if self.ratio is None or self.roi_w is None:
            raise Exception("ratio and roi_w is None")
        img_rows, img_cols = image.shape
        rows = int(img_rows / self.roi_w) + 0 if img_rows % self.roi_w == 0 else 1
        cols = int(img_cols / self.roi_w) + 0 if img_cols % self.roi_w == 0 else 1
        thr_map = np.zeros_like(image)
        for y in range(rows):
            for x in range(cols):
                xcor = x * self.roi_w
                ycor = y * self.roi_w
                roi = image[ycor:ycor+self.roi_w, xcor:xcor+self.roi_w]
                roi_flat = roi.flatten()
                sort_roi = np.sort(roi_flat[roi_flat>0])
                thr_map[ycor:ycor+self.roi_w, xcor:xcor+self.roi_w] = np.mean(sort_roi[int(self.ratio*len(sort_roi)):len(sort_roi)])
        return thr_map
    
    def get_mode(self):
        if self.__dual_mode:
            return "Ref mode"
        else:
            return "Single pic mode"
        
    def has_filter(self):
        return (self.__filter is not None)
    
    def get_filtered_target_image(self):
        return self.filtered_target

    def get_filtered_ref_image(self):
        return self.filtered_ref

    def set_para(self, **kwargs):
        para = {}
        for k in kwargs:
            if k == 'iamge':
                if kwargs['image'] is not None:
                    para['image'] = kwargs['image']
                else:
                    raise ValueError("Image is None")
            elif k == 'roi_w':
                if type(kwargs['roi_w']) is int or type(kwargs['roi_w']) is float:
                    para['roi_w'] = kwargs['roi_w']
                else:
                    raise TypeError('roi_w is not float or int')
            elif k == 'ratio':
                if type(kwargs['ratio']) is int or type(kwargs['ratio']) is float:
                    para['ratio'] = kwargs['ratio'] 
                else:
                    raise TypeError('ratio is not float or int')
            elif k == '_filter':
                if issubclass(type(kwargs['_filter']), FrequencyDomainFilter):
                    para['_filter'] = kwargs['_filter']
                else:
                    raise TypeError("filter object is not a subclass of Filter")


        for k in para:
            if k == 'image':
                self.__image = para['image']
            elif k == 'roi_w':
                self.roi_w = para['roi_w']
            elif k == 'ratio':
                self.ratio = para['ratio']
            elif k == '_filter':
                self.__filter = para['_filter']
