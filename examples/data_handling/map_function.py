"""
Map Funcion
===========
This example shows how the map function can be used. It applys a given function to the signalaxes at all navigation coordinates.

.. _HS_map_function: https://hyperspy.org/hyperspy-doc/current/reference/api.signals/BaseSignal.html#hyperspy.api.signals.BaseSignal.map
"""

# %%
import lumispy as lum
import numpy as np

# %%
# Loading Exemplementary Data
# ---------------------------
#
# Choosing the spectrum at the navigation coordinates ``(15, 12)`` to see a spike
s = lum.data.asymmetric_peak_map()
s.axes_manager["x"].index = 15
s.axes_manager["y"].index = 12
s.plot()

# %%
# Max Function
# ------------
#
# Get the highest Intensity from every spectrum in the map
s_max = s.map(np.max, inplace=False)
s_max.axes_manager["x"].index = 15
s_max.axes_manager["y"].index = 12
s_max.plot()


# %%
# Defining Custom Function
# ------------------------
#
# You can also define your own function to be applied to every signalaxes in the map.
# We define a function that gives either a one or a zero depending on the max intensity of the spectrum.
def black_white(spectrum):
    if np.max(spectrum) > 100:
        return 1
    else:
        return 0


s_black_white = s.map(black_white, inplace=False)
s_black_white.axes_manager["x"].index = 15
s_black_white.axes_manager["y"].index = 12
s_black_white.plot()

# %%
# for more information about the map function see the `documentation <HS_map_function_>`__.
#
