"""
Peak identification
===================
In this example we will demonstrate how to identify peaks in a spectrum.


.. _HS_find_peaks: https://hyperspy.org/hyperspy-doc/current/reference/api.signals/Signal1D.html#hyperspy.api.signals.Signal1D.find_peaks1D_ohaver
"""

# %%
# Load examplary data
import lumispy as lum

s = lum.data.asymmetric_peak_map()
s.plot()

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
#
# It returns a structured array that contains ``position``, ``height`` and ``width`` of the found peaks.
peaks[0, 0]

# %%
# Plotting the found peak
# ^^^^^^^^^^^^^^^^^^^^^^^
#
# Now we will plot the found peaks. At one position, an plot for comparison the original map besides.
start = (
    peaks[0, 0]["position"][0] - peaks[0, 0]["width"][0] / 2
)  # define start pos of the peak
end = start + peaks[0, 0]["width"][0]  # define end pos of the peak

s.inav[0, 0].plot()
s.inav[0, 0].isig[start:end].plot()

# %%
# sphinx_gallery_thumbnail_number = 4
