"""
Remove Background
==================

This example removes the background from a dataset.
"""

import lumispy as lum
import matplotlib.pyplot as plt

# Load the data
cl1 = lum.data.asymmetric_peak_map()

# Display the original data

cl1.plot()
plt.close(1)

# Now we remove the background

cl2 = cl1.remove_background(signal_range=(550.0, 620.0), background_type="Offset")

# Display the background removed data

cl2.plot()
plt.close(3)

# %%
# sphinx_gallery_thumbnail_number = 2
