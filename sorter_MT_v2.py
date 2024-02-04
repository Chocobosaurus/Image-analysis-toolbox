#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 10:43:35 2024

@author: Misha
"""

from pathlib import Path
import numpy as np
import shutil
import re

dirname = '/Users/UZH-wezhon/Desktop/D12_MIP/bgsubtraction_median/'
dr = Path(dirname)

fnames = sorted([f for f in dr.iterdir() if f.suffix == '.tif'])

def find_ch(string):
    pattern = r"ch\d{2}"
    match = re.search(pattern, string)
    assert match is not None, f"{string} does not contain channel info"
    return match.group()

channels = [find_ch(f.stem) for f in fnames]

# Saves to /sorted under current wd
new_dir = Path('sorted')
print(f'Saving to {str(Path.cwd() / new_dir)}')
new_dir.mkdir()
for ch in np.unique(channels):
    print(f"processing {ch}")
    based = new_dir / ch
    g_files = [f for f, cur_ch in zip(fnames, channels) if cur_ch == ch]
#     print(channels)
    based.mkdir()
    for f in g_files:
        shutil.copy(f, based / f.name)
            
fnames[0].name




