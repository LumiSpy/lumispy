"""
Remove Pixels
==================

This example removes pixels from a dataset.
"""

import lumispy as lum
import matplotlib.pyplot as plt

# Load the data
cl1 = lum.data.asymmetric_peak_map()
cl1 = cl1.remove_background(signal_range=(550.0, 620.0), background_type="Offset")

# Display the original data

cl1.plot()
plt.close(1)

# The signal beyond 800 nm goes to negative values, so lets remove the last three pixels from every spectrum:

cl2 = cl1.isig[:-3]

# Display cleaned data

cl2.plot()
plt.close(3)
# %%
# sphinx_gallery_thumbnail_number = 2
