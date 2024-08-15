# Alignment of 4i images based on landmarks

Python script for aligning query images onto reference images of 4i.
Query and reference images share one common channel ("landmark") as a clue of alignment.
DAPI may be a good option of the landmark channel.
Query and reference may have different numbers of channels but must be recorded at the same set of locations.

Query landmark image will be shifted in x-y direction to maximize its correlation with the reference landmark image.
The same x-y shift will be applied to the other channels of query. The shifted images are saved to an output folder.


## Installation

Download [script files](https://github.com/masashi-CU/4i-align/archive/refs/tags/v0.3.zip) and unpack.

Create conda environment.
```
conda create -n 4i-align scikit-image numpy pandas
conda activate 4i-align
```

## Prepare input
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

## Usage
```
python 4i-align.py <reference_folder> <query_folder> <output_folder>
```


 
