#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 9 22:46:49 2024

@author: UZH-wezhon
"""

import os
import numpy as np
from skimage import io
channelname = "ch01"

# Set the path to the folder containing z-stack images
input_path = '/Users/UZH-wezhon/Desktop/Auri_exp2_sorted/' \
              '230406 63x Exp 2_F4L_1_20_cmle_batch/ch01'

# Get a list of all image files in the folder
image_files = [f for f in os.listdir(input_path) if f.endswith('.tif')]

# Load the z-stack images
z_stack = [io.imread(os.path.join(input_path, f)) for f in image_files]

# Compute maximal projection
max_projection = np.max(np.array(z_stack), axis=0)

# Save the result as a lossless TIFF file
output_filename = os.path.join(os.path.dirname(input_path), channelname) + "_MAX.tif"
io.imsave(output_filename, max_projection.astype(np.uint16), plugin='tifffile', compression=0)




