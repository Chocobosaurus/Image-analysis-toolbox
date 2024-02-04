#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:50:38 2024

@author: UZH-wezhon
"""

import matplotlib.pyplot as plt
import numpy as np
import pywt
import os
from skimage import (
    color, restoration, util, io
)

plt.figure(figsize=(10, 6), dpi=300)


# Base folder containing all TIFF files
image = io.imread('/Users/UZH-wezhon/Desktop/test/20231221seedinginSHC1C2D3_w_B02_f_001_cmle_batch_ch03_MAX.tif'
                  , as_gray=True)

print("image loaded")


def plot_result(image, background):
    fig, ax = plt.subplots(nrows=1, ncols=3)

    ax[0].imshow(image, cmap='gray')
    ax[0].set_title('Original image')
    ax[0].axis('off')

    ax[1].imshow(background, cmap='gray')
    ax[1].set_title('Background')
    ax[1].axis('off')

    ax[2].imshow(filtered_image, cmap='gray')
    ax[2].set_title('Result')
    ax[2].axis('off')

    fig.tight_layout()

background = restoration.rolling_ball(image, radius=100)
print("background computed")
filtered_image = image - background

plot_result(image, background)
plt.show()




