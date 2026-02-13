"""
Remove Background
==================

This example removes the background from a dataset.
"""

# %%
# Load the data
import lumispy as lum
import matplotlib.pyplot as plt

cl1 = lum.data.asymmetric_peak_map()

# %%
# Display the original data

cl1.plot()
plt.close(1)

# %%
# Now we remove the background and display the data

cl2 = cl1.remove_background(signal_range=(550.0, 620.0), background_type="Offset")

cl2.plot()
plt.close(1)

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 2
# sphinx_gallery_end_ignore
