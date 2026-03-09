"""
Peak width determination
========================
This example demonstrates how to determine the width of a peak in a spectrum.

.. _HS_estimate_peak_width: https://hyperspy.org/hyperspy-doc/current/reference/api.signals/Signal1D.html#hyperspy.api.signals.Signal1D.estimate_peak_width
"""

# %%
import lumispy as lum

# load the data that we will use
s = lum.data.asymmetric_peak_map()
s.plot()

# %%
# Width Determination
# -------------------
#
# Estimates the width of the highest intensity peak of the spectra at a given fraction of its maximum. The default fraction is 0.5, this value can be set via ``factor``.
# With ``return_interval=True`` the function returns two extra signals with the positions of the desired height fraction at the left and right of the peak, see `doc <HS_estimate_peak_width_>`__.
width = s.estimate_peak_width(return_interval=True)

# %%
# Return Value
# ^^^^^^^^^^^^
# Returns float or lists of floats: ``[width, left, right]``. We update our metadata of the new signal containing our FWHM's and plot the results.
width[0].metadata.Signal.quantity = (
    "width"  # Since we dont have Intensity values anymore
)
width[0].plot(cmap="viridis")

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 3
# sphinx_gallery_end_ignore
