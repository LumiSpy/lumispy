"""
Remove Background
==================

This example removes the background from a dataset.
"""

import hyperspy.api as hs
import lumispy as lum
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Load the data from a file
file_path = Path.cwd().parent.parent / "lumispy" / "data" / "asymmetric_peak_map.hspy"

cl1 = hs.load(file_path)

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
