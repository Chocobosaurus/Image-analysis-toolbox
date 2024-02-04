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

# Load your image from the local folder
image_path = "/Users/UZH-wezhon/Desktop/Auri_exp1_sorted/" \
             "230404 63x Exp 1_Hm_1_10_cmle_batch/" \
             "230404 63x Exp 1_Hm_1_10_cmle_batchMAX_ch00.tif"  
             # Replace with the actual path to your image
input_folder, image_filename = os.path.split(image_path)
camera = io.imread(image_path, as_gray=True)  # Load the image in grayscale

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

# Save the figure 
# Create a relative path for the output file
output_folder = os.path.join(input_folder, "QC_classicalOtsu.png")
plt.savefig(output_folder, dpi=300, bbox_inches='tight')  # Adjust dpi and bbox_inches as needed

plt.show()

# Output the threshold value
print(f"Otsu's Threshold Value: {val}")
