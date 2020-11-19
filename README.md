# DeLIS

This repository contains the source code to perform DeLIS a deep learning based intensity standardisation method.

The method is composed of three steps ![delis](/delis.png)

## Requirements

Some of the important requirements to perform the code are:
- python v3.6.4
- the repository of [intensity normalization](https://github.com/jcreinhold/intensity-normalization)
- [Synthseg](https://github.com/BBillot/SynthSeg)

However, this requirements can be fulfil downloading the following docker image
``` docker pull emilyesme/tf_delis ```

**Note:** The DeLIS method use tensorflow backend to use the Synthseg. Therefore, it is necessary to have at less 10gb of ram in the host computer

## Instructions

To use the DeLIS method it is **necessary** to have docker.io installed v19.03.8 or later and perform the following instructions

1. clone the repository
2. download the following image ``` docker pull emilyesme/tf_delis ```
3. Move the run_intensity.py and run_delis.py to the data folder
4. To bind the docker container to the folder data, use 
```docker run -it --mount type=bind,src=/path/to/repository/data,dst=/data emilyesme/tf_delis```

## Usage

To use the DeLIS method, here is an example with run_delis.py in the data folder:

``` run_delis.py -b mri_image_1.nii.gz -o /data/ ```

Instructions:

```
Usage:  /data/run_delis.py
        -b path to MRI T1-w scan (nii or nii.gz file)
        -o output directory

```
