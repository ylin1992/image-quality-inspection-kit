# Demo GUI
This project contains 2 demo gui (so far), one of which is a filter tuner demo app and another is a detection tuner for real-world AR / VR blemish detection approaches. <br /><br />

All of the two demos are based on backend's services (BlemishDetectionService and FilterService)

# How to use
**Install Dependencies:** Go to the root directory and install dependencies by ```pip3 install -r requirements.txt```
**Modify main file:** In the ```main.py``` file, pick one of the demos and command out the others <br />
**Run the app** run ```python3 main.py```

# UI description:
## IQI Filter tuner
The tuner provides a visualized interface containing:
- Input raw image
- Real part of Fourier-Domain filter
- Image after being applied the filter
- A binarized result image by thresholding

![demo_gui_filter_tuner](https://github.com/ylin1992/image-quality-inspection-kit/blob/main/screenshot/IQI_filter_tuner.png)

***Load an image:*** Load an image (ends with jpg, png or bmp) from **File->Open Image** <br />
***Pick a filter type:***  Pick a filter type from the scroll-down menu. The toolbox provides below filter so far:
- Butterworth filter
- Gaussian filter
- Laplacian of Gaussian filter(used in other application)

***Specify the band type and bandwidth for the filter:*** There are 3 band types of each filter:
- Low pass, specify cutin frequency
- High pass, specify cutoff frequency
- Band pass, sepcify cutin and cutoff frequenct

***Check filter:*** After filter parameter are all set, click the **"Check Filter"** button under the top left figure in which a filter in frequency domain will be drawn subsequently.
**Note:** The filter size is (100, 100) by default if the raw image is not loaded. If the image is loaded, the filter will be set with the raw image's size.

***Apply filter:*** After the filter is generated, click apply filter, an image in space domain will be generated in the third (bottom left) canvas. You canzoom in a specific ROI to do pixel-level peeking

***Thresholding:*** After examining the filtered image, you might have a brief idea on how much threshold you should set to the filtered image so that you can seperate unwanted background noise and the real blemish signal. Specify a value and click **"Apply Threshold"** button at the bottom right corner.
<br />

## Detection tuner
The detection tuner provides a work flow how an optical engineer or quality control engineer works on determining a suitable filter parameter used in AOI on a new product's production lines.  
![demo_gui_dection_tuner](https://github.com/ylin1992/image-quality-inspection-kit/blob/main/screenshot/detection_tuner.png)

The app provides two modes for particle detection: **Single mode** and **Dual mode**.
- ***Single mode:*** Single mode needs a single DUT(Device Under Tested) image, the image applies a filter specified on the UI, and finally will be binarized by a threshold.
- ***Dual mode:*** Dual mode needs two images, one is the DUT image mentioned above, another is a reference image acting as a "standard" which helps sperarate unwanted noise and real blemish.
- ***Difference:*** Images captured through a VR lens tube strongly suffer from two major noises we don't want:
  - **Moire pattern:** caused by the frequency overlapping bewteen image sensor and VR panel's pixels.
  - **Black matrix pattern:** VR panels are usually LCD or AMOLED, both of which have pixels aligned periodically. If we look through the lens, the periodically aligned pixels will be "stretched" along the radius direction of the lens because of the distortion from the lens (usually over 30%), which makes the black matrix pattern more obvious. If you take a closer look at the first image of the screenshot, you may see a "cross-like" pattern at the center of the image, that is what we call black matri pattern noise <br /><br />

Above all, we still need to take care of the disuniformity of clarity across the VR's view of field (You can simply imagine that for a single dot, it is imaged differently at the center and at the outer field through a VR lens. The one at the center is siginificantly clearer than the outer one is). <br />

Based on the difference mentioned above, one approach is to take a standard image and let the program know at specific regions, the threshold should be set higher (or lower), hence the dual mode being used.

***Select a mode:*** Specify a mode from the scroll down menu.
<br />
<br />
***Load image(s):*** Load DUT image only if Single mode is selected. Load additional Ref Image if dual mode is selectde.
<br />

***Specify filter:*** Specify a filter with the options provided, remeber to click **Update Filter** button to setup the filter, you can click **Show filter** to take a look at the filter.
<br />

***Specify thresholding parameter:***
- Single mode: Specify threshold value
- Dual mode: Modify ratio and roi_w and threhold
<br />

***Start detection:*** Hit the ***"DETECT"*** button to start and get the result
