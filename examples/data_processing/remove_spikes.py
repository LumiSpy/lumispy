"""
Remove Spikes
==================

This example shows how to remove spikes from a dataset.
"""

import lumispy as lum

# Load the data
cl1 = lum.data.asymmetric_peak_map()
cl1 = cl1.remove_background(signal_range=(550.0, 620.0), background_type="Offset")
cl1 = cl1.isig[:-3]

# Display the original data

cl1.inav[29, 0].plot()

# As seen there is a heavy spike, so lets remove it:

cl1.spikes_removal_tool(interactive=False)

# Display cleaned data

cl1.inav[29, 0].plot()
# %%
# sphinx_gallery_thumbnail_number = 2
