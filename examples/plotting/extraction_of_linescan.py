"""
Extraction of linescan
==================

This example shows how to extract a linescan from a map using a ROI.
"""

# %%
# Load the data from a file
import lumispy as lum
import hyperspy.api as hs
import numpy as np

cl1 = lum.data.nanoparticles()

cl2 = cl1.T.mean()
cl2.data = cl2.data.astype(np.float32)

# %%
# First Intialize Line-ROI (region of interest) from position (5150, 4550) to position (5750, 4000) of width 20 in calibrated axes units:

line_roi = hs.roi.Line2DROI(5150, 4550, 5750, 4000, 20)
cl2.plot()
line_roi2 = line_roi.interactive(cl2, color="red")  # to show the ROI on the plot

# %%
# Extract data along the ROI as new signal profile by “slicing” the signal and plot the profile:

profile = line_roi(cl2)
profile.plot()

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 1
# sphinx_gallery_end_ignore
