# 4i-align.py (version 0.3)
# Written by Masashi Fujita <mf3362@cumc.columbia.edu>
# Feb 22, 2024

from skimage import io
from skimage import color
from skimage import registration
from skimage import transform
from skimage import util
import sys
from pathlib import Path
import re
import numpy as np
import pandas as pd

# reference_dir = "T5668_1"
# moving_dir = "T5668_2"
# output_dir = "T5668_2_aligned"

args = sys.argv
reference_dir = args[1]
moving_dir = args[2]
output_dir = args[3]

###############################################################################################

def apply_registering_transform(mov_img, tform):
    img_transformed = transform.warp(mov_img, tform)
    return(util.img_as_uint(img_transformed))

def get_registering_transform(ref_file, mov_file):
    ref_img = io.imread(ref_file)
    mov_img = io.imread(mov_file)
    shift = registration.phase_cross_correlation(ref_img, mov_img, return_error = False)
    tform = transform.EuclideanTransform(translation=[-shift[1], -shift[0]])

    # compute correlation coefficient after registration
    reg_img = apply_registering_transform(mov_img, tform)
    corr = np.corrcoef(ref_img.flatten(), reg_img.flatten())[0, 1]

    return([tform, shift, corr])

# function for reading 'images.csv'
def read_image_df(dir_path):
    img_df_file = dir_path.joinpath("images.csv")

    # check if 'images.csv' exists
    if not img_df_file.exists():
        raise FileNotFoundError(img_df_file)
    df = pd.read_csv(img_df_file)

    # check column names
    if not 'Spot' in df.columns:
        raise RuntimeError("Missing 'Spot' column in " + str(img_df_file))
    if not 'Landmark' in df.columns:
        raise RuntimeError("Missing 'Landmark' column in " + str(img_df_file))
    if not 'File' in df.columns:
        raise RuntimeError("Missing 'File' column in " + str(img_df_file))

    # check if all Files exist
    for file in df.File:
        file_path = dir_path.joinpath(file)
        if not file_path.exists():
            raise FileNotFoundError(file_path)

    # check if each Spot has one Landmark
    lm = df.groupby('Spot').value_counts(['Landmark'])
    if df[df.Landmark.notna()].query('Landmark != "Yes"').size > 0:
        raise RuntimeError('Landmark other than "Yes" was found in ' + str(img_df_file))
    if lm.max() > 1:
        raise RuntimeError('Spot with multiple Landmark was found in ' + str(img_df_file))
    if df.Spot.unique().size > lm.size:
        raise RuntimeError('Spot without Landmark was found in ' + str(img_df_file))

    return(df)

###############################################################################################

ref_path = Path(reference_dir)
mov_path = Path(moving_dir)
out_path = Path(output_dir)

# read image dataframe
ref_image_df = read_image_df(ref_path)
mov_image_df = read_image_df(mov_path)

if any(~mov_image_df.Spot.isin(ref_image_df.Spot)):
     raise RuntimeError('Missing moving Spot in reference images.csv')

# create output dir
if not out_path.exists():
    out_path.mkdir()

# data frame for landmark images and translation
df = pd.DataFrame()

# iterate over spots
landmark_image_df = ref_image_df[~ref_image_df.Landmark.isna()].merge(mov_image_df, on = ['Spot', 'Landmark'], suffixes = ('_ref', '_mov'))
for _, row in landmark_image_df.iterrows():
    ref_c0_file = ref_path.joinpath(row.File_ref)
    mov_c0_file = mov_path.joinpath(row.File_mov)

    # find transformation
    tform, shift, corr = get_registering_transform(ref_c0_file, mov_c0_file)

    # store translation info
    df_row = pd.DataFrame({
        'reference_image' : ref_c0_file,
         'moving_image' : mov_c0_file,
          'shift_x' : shift[0], 'shift_y' : shift[1], 'pixel_pearson_correlation' : [corr]
        })
    df = pd.concat([df, df_row])

    # list moving files at the position
    for mov_file in mov_image_df.query('Spot == {}'.format(row.Spot)).File:
        # load a moving image        
        mov_img = io.imread(mov_path.joinpath(mov_file))

        # apply registration
        reg_img = apply_registering_transform(mov_img, tform)

        # save registered image
        out_file = out_path.joinpath(mov_file)
        io.imsave(fname = out_file, arr = reg_img, check_contrast = False)

# save data frame
out_csv = out_path.joinpath("alignment-statistics.csv")
df.to_csv(out_csv, index = False)
