import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time
from skimage import io
from skimage.filters import threshold_multiotsu
import os

start = time.time()
# Setting the font size for all plots
matplotlib.rcParams['font.size'] = 9

# Load your image from the local folder
image_path = "/Users/UZH-wezhon/Desktop/Auri_exp1_sorted/" \
             "230404 63x Exp 1_WT_4_27_cmle_batch/" \
             "230404 63x Exp 1_WT_4_27_cmle_batchMAX_ch00.tif"  
             # Replace with the actual path to your image
input_folder, image_filename = os.path.split(image_path)

image = io.imread(image_path, as_gray=True)  # Load the image in grayscale

# Applying multi-Otsu threshold for the default value, generating three classes
print('Loaded file: ', image_path)
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

# Save the figure 
# Create a relative path for the output file
output_folder = os.path.join(input_folder, "QC_multiOtsu.png")
plt.savefig(output_folder, dpi=300, bbox_inches='tight')  # Adjust dpi and bbox_inches as needed

plt.show()

# Output the threshold values
print("Multi-Otsu Threshold Values:", thresholds)
end = time.time()
print("Program elapsed time = ", end - start)
time.process_time()
