# Demo GUI
This project contains 2 demo gui (so far), one of which is a filter tuner demo app and another is a detection tuner for real-world AR / VR blemish detection approaches. <br /><br />

All of the two demos are based on backend's services (BlemishDetectionService and FilterService)

# How to use
**Install Dependencies:** Go to the root directory and install dependencies by ```pip3 install -r requirements.txt```
**Modify main file:** In the ```main.py``` file, pick one of the demos and command out the others
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