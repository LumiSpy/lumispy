"""
Centroid / Center of Mass
=========================
This example shows how to determine the centroid of a peak.


.. _LS_centroid: https://docs.lumispy.org/en/stable/api/lumispy.signals.luminescence_spectrum.html#lumispy.signals.luminescence_spectrum.LumiSpectrum.centroid
"""

# %%
# Load examplary data
import lumispy as lum

s = lum.data.asymmetric_peak_map()
s.plot()

# %%
# Center Position
# ---------------
#
# Since the highest intesity value of a peak might not always be the most meanigful
# value to determin. Lumispy provides the `centroid() <LS_centroid_>`__ function which determines
# the center of mass of the peak.
com = s.centroid()

# %%
# Return Value
# ^^^^^^^^^^^^
# The return value is a new signal. In this case a Signal2D, which we can be plottet as a colormap:
com.plot(cmap="viridis")

# %%
# sphinx_gallery_thumbnail_number = 3
