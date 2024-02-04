#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 21:13:54 2024

@author: UZH-wezhon
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read data from Excel file
file_path = '/Users/UZH-wezhon/Desktop/wtmNLS_L.xlsx'
df = pd.read_excel(file_path)
sheet_name = 'diff_exp_analysis'

df = pd.read_excel(file_path, sheet_name=sheet_name)

fold_change = df['diff'].values
p_values = df['FDR'].values

fold_change_threshold = 2
p_value_threshold = 0.05

significant_down = (fold_change < -fold_change_threshold) & (p_values < p_value_threshold)
significant_up = (fold_change > fold_change_threshold) & (p_values < p_value_threshold)
non_significant = ~significant_down & ~significant_up

# Create a volcano plot
plt.figure(figsize=(8, 8))

plt.scatter(fold_change[non_significant], -np.log10(p_values[non_significant]), color='black', label='Non-significant')
plt.scatter(fold_change[significant_down], -np.log10(p_values[significant_down]), color='orange', label='WT')
plt.scatter(fold_change[significant_up], -np.log10(p_values[significant_up]), color='#3399ff', label='mNLS')

plt.xlabel('Fold Change')
plt.ylabel('-log(FDR)')
#plt.title('Volcano Plot')

plt.axvline(x=-fold_change_threshold, color='red', linestyle='--', label='Fold Change Threshold')
plt.axvline(x=fold_change_threshold, color='red', linestyle='--')

plt.axhline(y=-np.log10(p_value_threshold), color='green', linestyle='--', label='-log(FDR) Threshold')

plt.legend()

plt.savefig('volcano_plot.png', dpi=300) 

plt.show()
