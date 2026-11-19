"""
Centroid (center of mass)
=========================

This example uses :meth:`~lumispy.signals.luminescence_spectrum.LumiSpectrum.centroid`
to determine the intensity-weighted mean position of a luminescence peak.
The centroid can be useful for asymmetric peaks.
"""

# %%
import lumispy as lum

# Load a spectrum image containing asymmetric peaks.
s = lum.data.asymmetric_peak_map()
s.plot()

# %%
# Calculate the centroid at each navigation position and plot the result.
centroid = s.centroid()
centroid.plot(cmap="viridis")

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 2
# sphinx_gallery_end_ignore
