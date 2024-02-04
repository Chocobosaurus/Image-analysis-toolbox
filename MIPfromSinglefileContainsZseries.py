#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 19:00:11 2024

@author: UZH-wezhon
"""

import os
import numpy as np
from skimage import io

# Base folder containing all TIFF files
base_folder = '/Volumes/customer/data/w.zhong/SeedinginC1C2_2023Dec/1222d3decon/tiff'

# Folder to save MIP files
mip_folder = os.path.join(os.path.dirname(base_folder), 'MIP')

# Create the MIP folder if it doesn't exist
os.makedirs(mip_folder, exist_ok=True)

# Iterate over TIFF files in the base folder
for tiff_file in os.listdir(base_folder):
    tiff_file_path = os.path.join(base_folder, tiff_file)
    
    # Check if the current item is a TIFF file
    if os.path.isfile(tiff_file_path) and tiff_file.endswith('.tif'):
        print("Processing TIFF file:", tiff_file)
        
        # Load the z-stack images from the TIFF file
        z_stack = io.imread(tiff_file_path)
        
        # Compute maximal projection
        max_projection = np.max(z_stack, axis=0)
        
        # Construct the output filename in the MIP folder
        output_filename = os.path.join(mip_folder, os.path.splitext(tiff_file)[0] + "_MAX.tif")
        
        # Save the result as a lossless TIFF file
        io.imsave(output_filename, max_projection.astype(np.uint16), plugin='tifffile', compression=0)
        
        print("MIP saved for file:", tiff_file)
