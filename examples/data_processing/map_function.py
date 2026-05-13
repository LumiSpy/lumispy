"""
Map Function
===========
This example shows how the :py:meth:`~hyperspy.api.signals.BaseSignal.map` function can be used. It applies a given function to the ``signal axes`` at all navigation coordinates.

.. _HS_map_function: https://hyperspy.org/hyperspy-doc/current/reference/api.signals/BaseSignal.html#hyperspy.api.signals.BaseSignal.map
"""

# %%
import lumispy as lum
import numpy as np

# %%
# Loading exemplary data
# ---------------------------
#
# Choosing the spectrum at the navigation coordinates ``(15, 12)`` where a spike is visible.
s = lum.data.asymmetric_peak_map()
s.axes_manager.indices = (15, 12)
s.plot()

# %%
# Max function
# ------------
#
# Get the highest intensity from every spectrum in the map. This can also be done
# using the build in function :py:meth:`~hyperspy.api.signals.BaseSignal.max`.
s_max = s.map(np.max, inplace=False)  # s.max() would do the same
s_max.axes_manager.indices = (15, 12)
s_max.plot()


# %%
# Defining custom functions
# -------------------------
#
# You can also define your own functions to be applied to every signal axis in the map.
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
# For simple functions like the one above, you can also use a lambda function.
s_lambda = s.map(lambda x: 1 if x.max() > 100 else 0, inplace=False)
s_lambda.axes_manager.indices = (15, 12)
s_lambda.plot()

# %%
# For more information about the map function see the HyperSpy `documentation <HS_map_function_>`__.

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 3
# sphinx_gallery_end_ignore
