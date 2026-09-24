"""
Peak identification
===================
In this example we will demonstrate how to identify peaks in a spectrum.
"""

# %%
import lumispy as lum

# load the data that we will use
s = lum.data.asymmetric_peak_map()
s.plot()

# %%
# Peak identification
# -------------------
#
# Peaks can be identified and characterized using :py:meth:`~hyperspy.api.signals.Signal1D.find_peaks1D_ohaver`.
# With ``maxpeakn=1`` we only search for the highest peak in every spectrum of the map.
peaks = s.find_peaks1D_ohaver(maxpeakn=1)

# %%
# Return value
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

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 4
# sphinx_gallery_end_ignore
