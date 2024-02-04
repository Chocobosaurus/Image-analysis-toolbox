#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 19:28:01 2024

@author: UZH-wezhon
"""
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage import exposure, img_as_uint

# Load images
image_A_path = "/Users/UZH-wezhon/Desktop/Auri_exp2_sorted/" \
             "230406 63x Exp 2_F4L_4_23_cmle_batch/" \
             "230406 63x Exp 2_F4L_4_23_cmle_batchMAX_ch00.tif" 
image_B_path = "/Users/UZH-wezhon/Desktop/Auri_exp2_sorted/" \
             "230406 63x Exp 2_F4L_4_23_cmle_batch/" \
             "230406 63x Exp 2_F4L_4_23_cmle_batchMAX_ch00.tif" 
             #6M_1_20 
             
# Load images as 16-bit
imageA = img_as_uint(io.imread(image_A_path))
imageB = img_as_uint(io.imread(image_B_path))
           
# Perform histogram matching
matched_imageB = exposure.match_histograms(imageB, imageA)

# Report histogram of reference, source and match
hist_A, _ = np.histogram(imageA.flatten(), bins=65536, range=[0, 65535])
print("Histogram of reference: ", hist_A)
hist_B, _ = np.histogram(imageB.flatten(), bins=65536, range=[0, 65535])
print("Histogram of source: ", hist_B)
hist_matchedB, _ = np.histogram(matched_imageB.flatten(), bins=65536, range=[0, 65535])
print("Histogram of match: ", hist_matchedB)

# Calculate cumulative distributions of source and match
cdf_imageB = np.cumsum(np.histogram(imageB.flatten(), bins=65536, range=[0, 65535])[0])
cdf_matched_imageB = np.cumsum(np.histogram(matched_imageB.flatten(), bins=65536, range=[0, 65535])[0])
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
plt.show()

# Find the corresponding value to 10000 in the histogram distribution
target_bin = 10000

value = cdf_matched_imageB[target_bin]
print(f"Value to be matched for thereshold = {target_bin}: ", value)
source_bin = np.argmin(np.abs(cdf_imageB - value))
print("Target threshold value:", source_bin)











