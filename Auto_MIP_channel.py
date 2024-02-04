#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 23:29:48 2024

@author: UZH-wezhon
"""

import os
import numpy as np
from skimage import io

# Base folder containing subfolders named by image
base_folder = '/Users/UZH-wezhon/Desktop/Auri_exp3_sorted/'

# Iterate over subfolders in the base folder (each subfolder corresponds to an image)
for image_folder in os.listdir(base_folder):
    image_folder_path = os.path.join(base_folder, image_folder)
    
    # Check if the current item is a subfolder
    if os.path.isdir(image_folder_path):
        print("Checking image folder:", image_folder)
        # Iterate over possible channel names (from 'ch00' to 'ch03')
        for channel_index in range(4):
            channel_name = f'ch{channel_index:02d}'
            
            channel_folder_path = os.path.join(image_folder_path, channel_name)
            
            # Check if the current channel folder exists
            if os.path.isdir(channel_folder_path):
                print("Checking channel:", channel_name)
                # Get a list of all image files in the channel subfolder
                image_files = [f for f in os.listdir(channel_folder_path) if f.endswith('.tif')]
                
                # Load the z-stack images
                z_stack = [io.imread(os.path.join(channel_folder_path, f)) for f in image_files]
                
                # Compute maximal projection
                max_projection = np.max(np.array(z_stack), axis=0)
                
                # Save the result as a lossless TIFF file
                output_filename = os.path.join(image_folder_path, channel_name) + "_MAX.tif"
                io.imsave(output_filename, max_projection.astype(np.uint16), plugin='tifffile', compression=0)
                print("MIP saved for channel:", channel_name)
