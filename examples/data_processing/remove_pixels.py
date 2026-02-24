"""
Remove Pixels
=============

This example removes pixels from a dataset.
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
# The signal beyond 800 nm goes to negative values, so lets remove the last three pixels from every spectrum using :py:attr:`hyperspy.api.signals.BaseSignal.isig`.

cl2 = cl1.isig[:-3]

# %%
# Display cleaned data

cl2.plot()
plt.close(1)

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 2
# sphinx_gallery_end_ignore
