#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 15:12:32 2024

@author: UZH-wezhon
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Parameters
mean = 4433
std_dev = 1249

# Generate data points
x = np.linspace(mean - 4 * std_dev, mean + 4 * std_dev, 1000)
y = norm.pdf(x, mean, std_dev)

# Plot the normal distribution
plt.plot(x, y, label='Normal Distribution')
plt.title('Normal Distribution\nMean = 4433, Standard Deviation = 1249')
plt.xlabel('X-axis')
plt.ylabel('Probability Density Function (PDF)')
plt.legend()
plt.grid(True)
plt.show()
