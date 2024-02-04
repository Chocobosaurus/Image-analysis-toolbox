#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:50:38 2024

@author: UZH-wezhon
"""

import os
import split_image

# Base folder containing all TIFF files
base_folder = '/Users/UZH-wezhon/Desktop/D12_MIP/bgsubtraction_median'

# Folder to save splitted files
split_folder = os.path.join(os.path.dirname(base_folder), 'split')

# Create the result folder if it doesn't exist
# os.makedirs(split_folder, exist_ok=True)


# Iterate over TIFF files in the base folder
for tiff_file in os.listdir(base_folder):
    tiff_file_path = os.path.join(base_folder, tiff_file)
    
    # Check if the current item is a TIFF file
    if os.path.isfile(tiff_file_path) and tiff_file.endswith('.tif'):
        print("Processing TIFF file:", tiff_file)
        
        split_image.split_image(tiff_file_path, 3, 3, False, False, split_folder)
        # saving to assigned location function is not working
        
        
        
        