#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 3 12:20:43 2024

@author: UZH-wezhon
"""

import matplotlib.pyplot as plt
from skimage import io
import os
import sys
import numpy as np
from skimage import exposure, img_as_uint

def normalize(cdf):
    maxval = cdf[-1]
    return maxval, cdf.astype(float) / maxval

def process_image(input_path, output_txt):
    # Load reference image
    image_A_path = "/Users/UZH-wezhon/Desktop/test/" \
                   "230406 63x Exp 2_F4L_4_23_cmle_batch/ch00_MAX.tif" 
                 
    # Load images as 16-bit
    imageA = img_as_uint(io.imread(image_A_path))
    imageB = img_as_uint(io.imread(input_path))
    
    print('Loaded file:', input_path)           
    # Perform histogram matching
    matched_imageB = exposure.match_histograms(imageB, imageA)
    print("Starting to search for thresholds...", flush=True)
    
    # Report histogram of reference, source and match
    hist_A, _ = np.histogram(imageA.flatten(), bins=65536, range=[0, 65535])
    print("Histogram of reference: ", hist_A)
    hist_B, _ = np.histogram(imageB.flatten(), bins=65536, range=[0, 65535])
    print("Histogram of source: ", hist_B)
    hist_matchedB, _ = np.histogram(matched_imageB.flatten(), bins=65536, range=[0, 65535])
    print("Histogram of match: ", hist_matchedB)

    # Calculate cumulative distributions of source and match
    cdf_imageB = np.cumsum(np.histogram(imageB.flatten(), bins=65536, range=[0, 65535])[0])
    max_imageB, cdf_imageB = normalize(cdf_imageB)
    cdf_matched_imageB = np.cumsum(np.histogram(matched_imageB.flatten(), bins=65536, range=[0, 65535])[0])
    max_matched_imageB, cdf_matched_imageB = normalize(cdf_matched_imageB)
    
    print("CDF of source: ", cdf_imageB)
    print("CDF of match: ", cdf_matched_imageB)

    # Create a 2x2 subplot layout
    fig, axs = plt.subplots(2, 2, figsize=(12, 12), dpi = 300)

    # Plot the source image
    axs[0, 0].imshow(imageB, cmap='gray')
    axs[0, 0].set_title('Source Image')

    # Plot the reference image
    axs[0, 1].imshow(imageA, cmap='gray')
    axs[0, 1].set_title('Reference Image')

    # Plot the matched image
    axs[1, 0].imshow(matched_imageB, cmap='gray')
    axs[1, 0].set_title('Matched Image')

    # Plot histograms
    axs[1, 1].plot(cdf_imageB, color='blue', label='Original ImageB')
    axs[1, 1].plot(cdf_matched_imageB, color='red', label='Matched ImageB')
    axs[1, 1].set_title('Cumulative Distribution Functions')
    axs[1, 1].legend()

    plt.tight_layout()
    
    # Save the figure with the image file name included in the output path
    parent_dir_name = os.path.basename(os.path.dirname(input_path))
    output_filename = f"{parent_dir_name}_{os.path.basename(input_path)}_QC_histogramMatching.png"

    # Create the QCplots directory if it doesn't exist
    qcplots_directory = os.path.join(parent_directory, "QCplots_histMatch")
    os.makedirs(qcplots_directory, exist_ok=True)
    output_path = os.path.join(qcplots_directory, output_filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')  # Adjust dpi and bbox_inches as needed

    plt.close()  # Close the plot to avoid multiple plots accumulating in memory


    # Find the corresponding value to 10000 in the histogram distribution
    target_bin = 10000

    value = cdf_matched_imageB[target_bin]
    print(f"Value to be matched for thereshold = {target_bin}: ", value)
    source_bin = np.argmin(np.abs(cdf_imageB - value))
    print("Target threshold value found:", source_bin)
   
    # Write in the adaptive thresholds to the output text file
    with open(output_txt, 'a') as file:
        file.write(f"{parent_dir_name}_{os.path.basename(input_path)}, {source_bin}\n")


def process_images_in_directory(parent_directory):
    print("Walking through folders...")
    # Create a single output text file for all subdirectories
    output_txt = os.path.join(parent_directory, "Summary_AdaptedThreshold.txt")

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
