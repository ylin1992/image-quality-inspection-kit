# IQI (Image Quality Inspection) Tool Box

## General
The toolbox contains a filter tuning framework in which filters and stain detection approaches have been widely used in AR and VR AOI (automated optical inspection) indsutry.<br /><br />

This project consists of a backend and two demo GUIs (keeps being updated), refer to each README file for more details.

![demo_gui_filter_tuner](https://github.com/ylin1992/image-quality-inspection-kit/blob/main/screenshot/IQI_filter_tuner.png)
![demo_gui_dection_tuner](https://github.com/ylin1992/image-quality-inspection-kit/blob/main/screenshot/detection_tuner.png)

## Purpose
Filter tuning has been one of the critical steps for AOI on AR/VR production lines. As resolution of AR/VR devices have been getting higher, it is getting more critical to inspect minuscle particles, stain and blemishes inside the optical modules of each AR/VR device.<br /><br />
In order to screen out particles inside of a lens tube (let's take VR headset as an example, but the concept applies to AR as well), a routine work flow of a quality control or optical engineer would be:
- Pick a camera system that matches AR/VR headset's resolution
- Capture image and process the image
- Determine digital filter type and parameter
- Apply parameter to production line for mass engineering verification test
  
The purpose of this toolbox is to provide a visualized interface that helps optical and quality control engineers pick a suitable filter type and parameter that is sufficient to screen out unwanted, abnormal or contaminated devices in a AOI manner.
