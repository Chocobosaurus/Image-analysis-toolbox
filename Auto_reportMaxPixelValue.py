#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 15:24:37 2024

@author: UZH-wezhon
"""

from skimage import io
import os
import sys
import numpy as np
from skimage import img_as_uint

def normalize(cdf):
    maxval = cdf[-1]
    return maxval, cdf.astype(float) / maxval

def calculate_intensity_ratio(imageA, imageB):
    # Calculate the sum of intensities for each image
    sum_intensity_A = np.sum(imageA)
    sum_intensity_B = np.sum(imageB)

    # Normalize the sum of intensities of image B to image A
    intensity_ratio = sum_intensity_B / sum_intensity_A

    return intensity_ratio

def process_image(input_path, output_txt):
    # Load reference image
    image_A_path = "/Users/UZH-wezhon/Desktop/test/" \
                   "230406 63x Exp 2_F4L_4_23_cmle_batch/ch00_MAX.tif" 
                 
    # Load images as 16-bit
    imageA = img_as_uint(io.imread(image_A_path))
    imageB = img_as_uint(io.imread(input_path))
    
    print('Loaded file:', input_path)           

    # Report the maximum pixel value for image B
    max_pixel_value_B = np.max(imageB)
    print("Max Pixel Value for Image B:", max_pixel_value_B)

    # Write max pixel value to the output text file
    with open(output_txt, 'a') as file:
        parent_dir_name = os.path.basename(os.path.dirname(input_path))
        file.write(f"{parent_dir_name}_{os.path.basename(input_path)}, {max_pixel_value_B}\n")

def process_images_in_directory(parent_directory):
    print("Walking through folders...")
    # Create a single output text file for all subdirectories
    output_txt = os.path.join(parent_directory, "Summary_normtoIntegratedIntensity.txt")

    # Get a list of subdirectories in the parent directory
    subdirectories = [d for d in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, d))]

    for subdir in subdirectories:
        # Join the parent_directory and subdir to get the full path of the subdirectory
        subdir_path = os.path.join(parent_directory, subdir)

        # Get a list of image files in the subdirectory
        image_files = [f for f in os.listdir(subdir_path) if f.endswith(('.tif', '.png', '.jpg')) 
                       and "MAX" in f and "ch00" in f and "QC" not in f]

        # Iterate over each image file in the subdirectory
        for image_file in image_files:
            # Create the full path of the input image file
            input_path = os.path.join(subdir_path, image_file)

            # Call the process_image function to process the image
            process_image(input_path, output_txt)

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py parent_directory")
        sys.exit(1)

    parent_directory = sys.argv[1]

    # Check if the parent directory is a valid directory
    if not os.path.isdir(parent_directory):
        print(f"Error: {parent_directory} is not a valid directory.")
        sys.exit(1)

    # Process images in all subdirectories of the parent directory
    process_images_in_directory(parent_directory)




