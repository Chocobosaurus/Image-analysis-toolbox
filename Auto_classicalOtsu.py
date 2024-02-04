#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 3 12:20:43 2024

@author: UZH-wezhon
"""

import matplotlib.pyplot as plt
from skimage import io
from skimage import filters
from skimage import exposure
import os
import sys

def process_image(input_path, output_txt):
    # Load your image from the input path
    camera = io.imread(input_path, as_gray=True)  # Load the image in grayscale

    val = filters.threshold_otsu(camera)

    hist, bins_center = exposure.histogram(camera)

    # Increase DPI and adjust figure size
    plt.figure(figsize=(12, 4), dpi=300)  # Adjust figsize and dpi as needed

    plt.subplot(131)
    plt.imshow(camera, cmap='gray', interpolation='nearest')
    plt.title('Original')
    plt.axis('off')

    plt.subplot(132)
    plt.imshow(camera < val, cmap='gray', interpolation='nearest')
    plt.title('Otsu Result')
    plt.axis('off')

    plt.subplot(133)
    plt.plot(bins_center, hist, lw=2)
    plt.axvline(val, color='k', ls='--')
    plt.title('Histogram')

    plt.tight_layout()

    # Save the figure with the image file name included in the output path
    parent_dir_name = os.path.basename(os.path.dirname(input_path))
    output_filename = f"{parent_dir_name}_{os.path.basename(input_path)}_QC_histogramMatching.png"

    # Create the QCplots directory if it doesn't exist
    qcplots_directory = os.path.join(parent_directory, "QCplots_classicalOtsu")
    os.makedirs(qcplots_directory, exist_ok=True)
    output_path = os.path.join(qcplots_directory, output_filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')  # Adjust dpi and bbox_inches as needed

    plt.close()  # Close the plot to avoid multiple plots accumulating in memory

    print(f"{val}")


    # Write only the numerical value of the Otsu threshold to the output text file
    with open(output_txt, 'a') as file:
        file.write(f"{parent_dir_name}_{os.path.basename(input_path)}, {val}\n")

def process_images_in_directory(parent_directory):
    print("Walking through folders...")
    print("Printing Otsu's Threshold Values: ")
    # Create a single output text file for all subdirectories
    output_txt = os.path.join(parent_directory, "Summary_ClassicalOtsuValues.txt")

    # Get a list of subdirectories in the parent directory
    subdirectories = [d for d in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, d))]

    for subdir in subdirectories:
        # Join the parent_directory and subdir to get the full path of the subdirectory
        subdir_path = os.path.join(parent_directory, subdir)

        # Get a list of image files in the subdirectory
        image_files = [f for f in os.listdir(subdir_path) if f.endswith(('.tif', '.png', '.jpg')) and "MAX" in f]

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
