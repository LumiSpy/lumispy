"""
Map Funcion
===========
This example shows how the map function can be used. It applys a given function to the signal data at all navigation coordinates.
"""

# %%
import lumispy as lum
import numpy as np

# %%
# Loading Exemplementary Data
s = lum.data.asymmetric_peak_map()
s.plot()

# %%
# Max Function
# ------------
#
# Get the highest Intensity from every spectrum in the map
s.max().plot()
