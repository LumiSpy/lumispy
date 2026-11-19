"""
Map function
============

This example uses :py:meth:`~hyperspy.api.signals.BaseSignal.map` to apply
a function to every spectrum in a map.
"""

# %%
import lumispy as lum
import numpy as np

# %%
# Load the example spectrum image and select a position with a visible spike.
s = lum.data.asymmetric_peak_map()
s.axes_manager.indices = (15, 12)
s.plot()

# %%
# Find the maximum intensity of each spectrum. The same result can be obtained
# using :py:meth:`~hyperspy.api.signals.BaseSignal.max`.
s_max = s.map(np.max, inplace=False)  # Equivalent to s.max().
s_max.axes_manager.indices = (15, 12)
s_max.plot()


# %%
# A custom function can also be mapped over the spectra. This function
# returns 1 if the maximum intensity exceeds 100 and 0 otherwise.
def black_white(spectrum):
    if np.max(spectrum) > 100:
        return 1
    else:
        return 0


s_black_white = s.map(black_white, inplace=False)
s_black_white.axes_manager.indices = (15, 12)
s_black_white.plot()

# %%
# For a short function, the same operation can be written as a lambda.
s_lambda = s.map(lambda x: 1 if x.max() > 100 else 0, inplace=False)
s_lambda.axes_manager.indices = (15, 12)
s_lambda.plot()


# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 3
# sphinx_gallery_end_ignore
