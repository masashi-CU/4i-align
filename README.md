# Alignment of 4i images based on landmarks

Python script for aligning query images onto reference images of 4i.
Query and reference images share one common channel ("landmark") as a clue of alignment.
DAPI may be a good option of the landmark channel.
Query and reference may have different numbers of channels but must be recorded at the same set of locations.

Query landmark image will be shifted in x-y direction to maximize its correlation with the reference landmark image.
The same x-y shift will be applied to the other channels of query. 

## Installation

1. Download [script files](https://github.com/masashi-CU/4i-align/archive/refs/tags/v0.3.zip), and unpack it.

2. Create conda environment.
```
conda create -n 4i-align scikit-image numpy pandas
conda activate 4i-align
```

## Prepare input
1. Create an empty folder for reference images.
2. Move reference image files into the reference folder. Images should be single-channel files.
3. Create a CSV file named ```images.csv``` that has three columns:
- Spot: recording locations. Multiple channels at the same location should have the same "Spot" value.
- Landmark: “Yes” for landmark channel.
- File: image file names.
4. Prepare query folder in the same way. "Spot" values of query and reference should the same if they were recorded at the same location.

## Usage
```
python 4i-align.py <reference_folder> <query_folder> <output_folder>
```
The shifted query images will be saved to the output folder.
