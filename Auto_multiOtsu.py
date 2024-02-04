#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 3 12:20:43 2024

@author: UZH-wezhon
"""
import matplotlib
import matplotlib.pyplot as plt
from skimage import io
from skimage.filters import threshold_multiotsu
import os
import sys
import numpy as np
import time

# Setting the font size for all plots
matplotlib.rcParams['font.size'] = 9

def process_image(input_path, output_txt):
    start = time.time()
    # Load your image from the input path
    image = io.imread(input_path, as_gray=True)  # Load the image in grayscale

    # Applying multi-Otsu threshold for the default value, generating three classes
    print('Loaded file:', input_path)
    print("Starting to search for thresholds...", end='', flush=True)
    thresholds = threshold_multiotsu(image)
    print("Done!!", flush=True)

    # Using the threshold values to generate the three regions
    regions = np.digitize(image, bins=thresholds)
    
    # Increase DPI for better resolution
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(15, 5), dpi=300)  # Adjust figsize and dpi as needed
    
    # Plotting the original image.
    ax[0].imshow(image, cmap='gray')
    ax[0].set_title('Original')
    ax[0].axis('off')
    
    # Plotting the histogram and the two thresholds obtained from multi-Otsu
    ax[1].hist(image.ravel(), bins=255)
    ax[1].set_title('Histogram')
    for thresh in thresholds:
        ax[1].axvline(thresh, color='r')
    
    # Plotting the Multi Otsu result
    ax[2].imshow(regions, cmap='jet')
    ax[2].set_title('Multi-Otsu result')
    ax[2].axis('off')
    
    plt.subplots_adjust()

    # Save the figure with the image file name included in the output path
    parent_dir_name = os.path.basename(os.path.dirname(input_path))
    output_filename = f"{parent_dir_name}_{os.path.basename(input_path)}_QC_histogramMatching.png"

    # Create the QCplots directory if it doesn't exist
    qcplots_directory = os.path.join(parent_directory, "QCplots_multiOtsu")
    os.makedirs(qcplots_directory, exist_ok=True)
    output_path = os.path.join(qcplots_directory, output_filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')  # Adjust dpi and bbox_inches as needed

    plt.close()  # Close the plot to avoid multiple plots accumulating in memory

    print("Multi-Otsu Threshold Values:", thresholds)
    end = time.time()
    print("Elapsed time for this image = ", end - start)
    time.process_time()

    # Write only the numerical values of the Multi-Otsu thresholds to the output text file
    with open(output_txt, 'a') as file:
        file.write(f"{parent_dir_name}_{os.path.basename(input_path)},  {', '.join(map(str, thresholds))}\n")


def process_images_in_directory(parent_directory):
    print("Walking through folders...")
    # Create a single output text file for all subdirectories
    output_txt = os.path.join(parent_directory, "Summary_MultiOtsuValues.txt")

    # Get a list of subdirectories in the parent directory
    subdirectories = [d for d in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, d))]

    for subdir in subdirectories:
        # Join the parent_directory and subdir to get the full path of the subdirectory
        subdir_path = os.path.join(parent_directory, subdir)

        # Get a list of image files in the subdirectory
        image_files = [f for f in os.listdir(subdir_path) if f.endswith(('.tif', '.png', '.jpg')) 
                       and "MAX" in f and "Otsu" not in f]

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
