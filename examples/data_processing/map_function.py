"""
Map Funcion
===========
This example shows how the ``map`` function can be used. It applys a given function to the signalaxes at all navigation coordinates.



.. _HS_map_function: https://hyperspy.org/hyperspy-doc/current/reference/api.signals/BaseSignal.html#hyperspy.api.signals.BaseSignal.map
"""

# %%
import lumispy as lum
import numpy as np

# %%
# Loading exemplary Data
# ---------------------------
#
# Choosing the spectrum at the navigation coordinates ``(15, 12)`` where a spike is visible.
s = lum.data.asymmetric_peak_map()
s.axes_manager.indices = (15, 12)
s.plot()

# %%
# Max Function
# ------------
#
# Get the highest Intensity from every spectrum in the map. This can also be done
# using the build in function ``max``.
s_max = s.map(np.max, inplace=False)  # s.max() would do the same
s_max.axes_manager.indices = (15, 12)
s_max.plot()


# %%
# Defining Custom Functions
# -------------------------
#
# You can also define your own functions to be applied to every signalaxes in the map.
# We define a function that gives either a one or a zero depending on the max intensity of the spectrum.
def black_white(spectrum):
    if np.max(spectrum) > 100:
        return 1
    else:
        return 0


s_black_white = s.map(black_white, inplace=False)
s_black_white.axes_manager.indices = (15, 12)
s_black_white.plot()

# %%
# For simple Functions like the one above, you can also use a lambda function.
s_lambda = s.map(lambda x: 1 if x.max() > 100 else 0, inplace=False)
s_lambda.axes_manager.indices = (15, 12)
s_lambda.plot()

# %%
# for more information about the map function see the `documentation <HS_map_function_>`__.

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 3
# sphinx_gallery_end_ignore
