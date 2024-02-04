#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 10:43:35 2024

@author: Misha
"""

from pathlib import Path
import numpy as np
import shutil

dirname = '/Users/UZH-wezhon/Desktop/MIP/originalfiles/bgsubtraction'
dr = Path(dirname)

fnames = sorted([f for f in dr.iterdir() if f.suffix == '.tif'])
groups = np.unique([f.stem[:-10] for f in fnames])

# Saves to /sorted under current wd
new_dir = Path('sorted')
print(f'Saving to {str(Path.cwd() / new_dir)}')
new_dir.mkdir()
for g in groups:
    based = new_dir / g
    g_files = [f for f in fnames if f.stem.startswith(g)]
    channels = np.unique([f.stem[-4:] for f in g_files])
#     print(channels)
    based.mkdir()
    for c in channels:
        curd = based / c
        curd.mkdir()
        cur_fnames = [f for f in g_files if f.stem.endswith(c)]
        for f in cur_fnames:
            shutil.copy(f, curd / f.name)
            
fnames[0].name




