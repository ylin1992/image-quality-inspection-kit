# Demo GUI
This project contains 2 demo gui (so far), one of which is a filter tuner demo app and another is a detection tuner for real-world AR / VR blemish detection. <br /><br />

All of the two demos are based on backend's services in the ```backend``` folder(BlemishDetectionService and FilterService)

# How to use
**Install Dependencies:** Go to the root directory and install dependencies by ```pip3 install -r requirements.txt``` <br />
**Modify main file:** In the ```main.py``` file, pick one of the demos and command out the others <br />
**Run the app:** run ```python3 main.py```

# UI description
## IQI Filter tuner
The tuner provides a user interface containing:
- Input raw image
- Real part of Fourier-Domain filter
- Image applying the filter
- A binarized result image by thresholding

![demo_gui_filter_tuner](https://github.com/ylin1992/image-quality-inspection-kit/blob/main/screenshot/IQI_filter_tuner.png)
![demo_gui_filter_tuner](https://github.com/ylin1992/image-quality-inspection-kit/blob/main/screenshot/filter_tuner_demo.gif)

***Load an image:*** Load an image (ends with jpg, png or bmp) from **File->Open Image** <br />
***Pick a filter type:***  Pick a filter type from the scroll-down menu. The toolbox provides below filters:
- Butterworth filter
- Gaussian filter
- Laplacian of Gaussian filter

***Specify the band type and bandwidth for the filter:*** There are 3 band types of each filter:
- Low pass, specify cutin frequency
- High pass, specify cutoff frequency
- Band pass, sepcify cutin and cutoff frequenct

***Check filter:*** After filter parameter are all set, click the **"Check Filter"** button under the top left figure in which a filter in frequency domain will be drawn subsequently. <br />
**Note:** The filter size is (100, 100) by default if the raw image is not loaded. If the image is loaded, the filter will be set with the raw image's size.

***Apply filter:*** After the filter is generated, click apply filter, an image in space domain will be generated in the third (bottom left) canvas. You can zoom in a specific ROI to do pixel-level peeking

***Thresholding:*** After examining the filtered image, you might have a brief idea on how much threshold you should set to the filtered image so that you can seperate unwanted background noise and the real blemish signal. Specify a value and click **"Apply Threshold"** button at the bottom right corner.
<br />

## Detection tuner
The detection tuner provides a work flow to how an optical engineer or quality control engineers work on determining a suitable filter parameter used in AOI for a new product's production lines.  
![demo_gui_dection_tuner](https://github.com/ylin1992/image-quality-inspection-kit/blob/main/screenshot/detection_tuner.png)
![demo_gui_dection_tuner](https://github.com/ylin1992/image-quality-inspection-kit/blob/main/screenshot/detection_tuner.gif)

The app provides two modes for particle detection: **Single mode** and **Dual mode**.
- ***Single mode:*** Single mode needs a single DUT(Device Under Tested) image, the image applies a filter specified on the UI, and finally will be binarized by a given threshold value.
- ***Dual mode:*** Dual mode needs two images, one is the DUT image mentioned above, another is a reference image acting as a "standard" which helps sperarate unwanted noise and real blemish.
- ***Why Daul Mode:*** Images captured through a VR lens tube strongly suffer from two major noises we don't want:
  - **Moire pattern:** caused by the frequency overlapping bewteen image sensor and VR panel's pixels.
  - **Black matrix pattern:** VR panels are usually LCD or AMOLED, both of which have pixels aligned periodically. If we look through the lens, the periodically aligned pixels are "stretched" along the radius direction of the lens due to the fact that a serious distortion of VR lens is usually unavoidable and that sagital MTF of a lens is generally better than the tangential one, which makes the black matrix pattern more obvious. If you take a closer look at the first image of the screenshot, you may see a "cross-like" pattern at the center of the image, that is what we call the **black matrix pattern** noise <br /><br />

Above all, we still need to take care of the disuniformity of clarity across the VR's view of field (simply imagine that for a single dot, it is imaged differently at the center and at the outer field through a VR lens. The one at the center is siginificantly clearer than the outer one). <br />

Based on the differences mentioned above, one approach is to take a standard image and let the program know that at specific regions, the threshold should be set higher (or lower), hence the dual mode being used.

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
