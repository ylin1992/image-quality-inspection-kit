# IQI Tuner Framework
The frameworks provides a series of filters and detection approaches for different image quality inspection application for AR and VR devices

## General
The frameworks can be borken down in two parts:
- Filters: Digital filters commonly used in image quality inspection.
- Detections: Detection approaches based on filters above

## Filters
All filters are abstract of ```FrequencyDomainFilter```, space domain filters are not implemented right now. <br />
Each filter has the following methods:
- ```FrequencyDomainFilter.get_filt() -> numpy.ndarray```: Retrieve a 2D filter in Fourier domain (real part)
- ```FrequencyDomainFilter.low_pass() -> numpy.ndarray```: Retrieve a 2D low pass filter based on the cutin frequency provided
- ```FrequencyDomainFilter.high_pass() -> numpy.ndarray```: Retrieve a 2D high pass filter based on the cutin frequency provided
- ```FrequencyDomainFilter.band_pass() -> numpy.ndarray```: Retrieve a 2D band pass filter based on the cutin frequency provided
- ```FrequencyDomainFilter.apply(image: numpy.ndarray) -> numpy.ndarray```: Apply the filter to the input image, the image will be converted to grey scale if the image has 3 channels. Return the filtered image (in space domain)
- ```FrequencyDomainFilter.set_shape(shape: tuple)```: Set filter's shape, len(shape) should be 2
- ```FrequencyDomainFilter.get_shape() -> tuple```: Returns filter's shape
- ```FrequencyDomainFilter.set_frequency_para(**kwargs)```: Set cutin, cutoff, sigma info for the filters, based on the filter's type
- ```FrequencyDomainFilter.get_frequency_para() -> dict```: Returns a dictionary containing frequency information like ```cutin```, ```cutoff```
- ```FrequencyDomainFilter.set_filter_type(str)```: Set band type of filter, input should be:
  - ```'lp'```: low pass
  - ```'hp'```: high pass
  - ```'bp'```: band pass
- ```FrequencyDomainFilter.get_filter_type() -> str```: Returns filter type in ```str```

## Detection
Stain detections are designed to detect stain which generally based on a ```FrequencyDomainFilter``` and an ```image```.  

All detections are abstract of ```StainDetection```, which have the following methods:
- ```StainDetection.start_calculate() -> kwargs```: Start the detection
- ```StainDetection.has_image() -> bool```: Returns ```True``` if the image is loaded.
- ```StainDetection.set_image(numpy.ndarray)```: Set the target image, image should be in gray
- ```StainDetection.get_image() -> numpy.ndarray```: Get target image
- ```StainDetection.get_filter() -> FrequencyDomainFilter```: Get a ```FrequencyDomainFilter``` object
- ```StainDetection.set_filter(FrequencyDomainFilter)```: Set a ```FrequencyDomainFilter``` object to the detection.
- ```StainDetection.set_para(**kwargs)```: Set additional parameter for detection.


# Services
Services layer provides interaction between model layer and client. There are two services so far.
- DetectionService
- FilterService

## FilterService
- ```get_gaussian_filter(shape, sigma_x, sigma_y, type, sigma_x2, sigma_y2) -> GaussianFilter```
  - ```shape```: filter's shape, should be ```(2, ) tuple```
  - ```sigma_x```: ```float```, sigma of Gaussian filter along x direction
  - ```sigma_y```: ```float```, sigma of Gaussian filter along y direction
  - ```type```: ```str```, band type of the filter, default is ```'lp'```, should be one of ```'lp', 'bp', 'hp'```
  - ```sigma_x2```: **optional**, cutoff frequency of sigma_x, only neccessary for band pass filter
  - ```sigma_y2```: **optional**, cutoff frequency of sigma_ym only neccessary for band pass filter

- ```get_butterworth_filter(shape, cutin, cutoff=0, type='bp') -> ButterworthFilter```
  - ```shape```: filter's shape, should be ```(2, ) tuple```
  - ```cutin```: cut in frequency (If using high pass filter, specify cutin is enough)
  - ```cutoff```: **optional**, cut off frequency for bandpass filter
  - ```type```: ```str```, band type of the filter, default is ```'bp'```, should be one of ```'lp', 'bp', 'hp'```

- ```get_filter_shape(filter: FrequencyDomainFilter) -> tuple```: get filter shape


## Example flow (single mode detection)
```
from backend.service.DetectionService import BlemishDetectionService
from backend.service import FilterService
import cv2
import matplotlib.pyplot as plt

im = cv2.imread('YOUR_IMAGE_PATH', 0)

# Generate a butterworth filter
filter = FilterService.get_butterworth_filter(shape=shape, cutin=0.03, cutoff=0.5, type='bp')

# generate a detection service object
detectionService = BlemishDetectionService(image=im, filter=filter)
detectionService.initBlemishDetectionObject()

res, _ = detectionService.start_calculate(thr=10)
plt.figure()
plt.imshow(res)
plt.figure()
plt.imshow(detectionService.get_filtered_target_image())
plt.show()
```

## Example flow (dual mode detection)
```
from backend.service.DetectionService import BlemishDetectionService
from backend.service import FilterService
import cv2
import matplotlib.pyplot as plt

im = cv2.imread('YOUR_IMAGE_PATH', 0)
im_ref = cv2.imread('YOUR_REF_IMAGE_PATH', 0)

# Generate a butterworth filter
filter = FilterService.get_butterworth_filter(shape=shape, cutin=0.03, cutoff=0.5, type='bp')

# generate a detection service object
detectionService = BlemishDetectionService(image=im, filter=filter, ref_image=im_ref, ratio=0.99, roi_w=100)
detectionService.initBlemishDetectionObject()

res, thr_map = detectionService.start_calculate(thr=10)
plt.figure()
plt.imshow(res)
plt.figure()
plt.imshow(thr_map)
plt.figure()
plt.imshow(detectionService.get_filtered_target_image())
plt.figure()
plt.imshow(detectionService.get_filtered_ref_image())
plt.show()
```