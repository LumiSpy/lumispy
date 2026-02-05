"""
Peak Analysis
=============
In this example, we will show different tools to find peaks, there center and their width. This can be usefull for asymmetric peaks, since fitting
might not always be the best option.

.. _HS_find_peaks: https://hyperspy.org/hyperspy-doc/current/reference/api.signals/Signal1D.html#hyperspy.api.signals.Signal1D.find_peaks1D_ohaver
.. _LS_centroid: https://docs.lumispy.org/en/stable/api/lumispy.signals.luminescence_spectrum.html#lumispy.signals.luminescence_spectrum.LumiSpectrum.centroid
.. _HS_estimate_peak_width: https://hyperspy.org/hyperspy-doc/current/reference/api.signals/Signal1D.html#hyperspy.api.signals.Signal1D.estimate_peak_width
"""

# %%
# Load examplary data
import lumispy as lum

s = lum.data.asymmetric_peak_map()

# %%
# Peak Identification
# -------------------
#
# Peaks can be identified and characterized using `find_peaks1D_ohaver() <HS_find_peaks_>`__.
# With ``maxpeakn=1`` we only search for the highest peak in every spectrum of the map.
peaks = s.find_peaks1D_ohaver(maxpeakn=1)

# %%
# Return Value
# ^^^^^^^^^^^^
# It returns a structured array that contains ``position``, ``height`` and ``width`` of the found peaks.
peaks[0, 0]

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
# The return value is a new signal. In this case a Signal2D, which we can plot as a colormap:
com.plot(cmap="viridis")

# %%
# Width Determination
# -------------------
#
# Estimates the width of the highest intensity peak of the spectra at a given fraction of its maximum. The default fraction is 0.5, this value can be set via ``factor``.
# With ``return_interval=True`` the function returns two extra signals with the positions of the desired height fraction at the left and right of the peak. `Doc <HS_estimate_peak_width_>`__.
width = s.estimate_peak_width(return_interval=True)

# %%
# Return Value
# ^^^^^^^^^^^^
# Returns float or lists of floats: ``[width, left, right]``. In our case we get a list of width since we have a map of spectra.
width[0].metadata.Signal.quantity = (
    "width"  # Since we dont have Intensity values anymore
)
width[0].plot(cmap="viridis")

# %%
# sphinx_gallery_thumbnail_number = 1
