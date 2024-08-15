# Alignment of 4i images based on landmarks

Python script and its example input.
Here is my Python script to align tiles. Its inputs are:

## Installation
```
conda create -n 4i-align skimage numpy pandas
git clone 
```

## Usage
In the command line, you will run the script, specifying reference folder, moving folder, and output folder.
% python align-tile-by-DAPI.py <reference_folder> <moving_folder> <output_folder>
Images in the moving folder will be read, shifted in x-y direction to maximize alignment of landmarks, and saved to output folder.

To specify relationship of images, please create two CSV files (images.csv), one in the reference folder, and another in the moving folder.
Spot: specifies corresponding locations between ref and mov.
Landmark: “Yes” shows DAPI
File: image file name

“Reference” folder for the first round of 4i images. Images are non-stitched, single-channel TIFF images. DAPI channels should have a suffix “_c0000.tif”. For example, files for three-channel imaging at two positions may be something like:
position0000_c0000.tif (DAPI)
position0000_c0001.tif
position0000_c0002.tif
position0001_c0000.tif (DAPI)
position0001_c0001.tif
position0001_c0002.tif
“Moving” folder for the second round of 4i images. Again, DAPI should be named “_c0000.tif”. If you did two-channel imaging, then files may be:
position0000_c0000.tif (DAPI)
position0000_c0003.tif
position0001_c0000.tif (DAPI)
position0001_c0003.tif
 
